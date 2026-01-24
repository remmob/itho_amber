"""Itho Daalderop Amber 65/95/120 Modbus Hub/coordinator."""

import time
import logging
import threading
import asyncio
import traceback
from datetime import timedelta, datetime

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ConnectionException, ModbusIOException
from homeassistant.components.persistent_notification import async_create as create_persistent_notification
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import CALLBACK_TYPE, callback, HomeAssistant

from .const import (
    DOMAIN, LOGIN_STATUS, ON_OFF_STATUS, PUMP_TYPE, CURRENT_OPERATION_MODE,
    EXTERNAL_CONTROL, HWTBH_PRIORITY_MODE, MODE_SIGNAL_TYPE, MODE_SIGNAL_OUTPUT,
    DISPLAY_TIME, FAILURE_STATUS, ACTIVE_STATUS)

_LOGGER = logging.getLogger(__name__)

MAX_READ_RETRIES = 3

class AmberModbusHub(DataUpdateCoordinator[dict]):
    """Thread safe wrapper class for pymodbus."""

    def __init__(self, hass: HomeAssistant, name: str, host: str, port: int | float, scan_interval: int | float, notify_connection_errors_mobile: bool = False, notify_connection_errors_persistent: bool = False, notify_services: str = "", notification_title: str = "Warmtepomp verbindingsfout!", connection_error_delay: int = 60):
        """Initialize the Itho Daalderop Amber 65/95/120 Modbus hub."""
        super().__init__(hass, _LOGGER, name=name, update_interval=timedelta(seconds=scan_interval))

        self._flush_running = False
        self._flush_pending = False
        self._ha_started = False
        self._write_queue = []
        self._write_timer = None
        self._modbus_lock = threading.Lock()
        self._lock = threading.Lock()
        self._client = None
        self._host = host
        self._port = int(port)
        self._consecutive_failures = 0  # Track consecutive connection failures
        self._last_successful_read = None  # Track last time we got valid data
        self._notify_connection_errors_mobile = notify_connection_errors_mobile
        self._notify_connection_errors_persistent = notify_connection_errors_persistent
        self._notify_services = notify_services
        self._notification_title = notification_title
        # Track sent notifications to avoid duplicates
        self._connection_error_notified = False
        self._connection_lost_time = None  # Track when connection was first lost
        self._last_partial_failure_details = ""
        # Calculate how many failures based on configured delay and scan_interval
        self._failures_for_delay = max(1, int(connection_error_delay / scan_interval))
        _LOGGER.debug(f"Connection error notification will be sent after {self._failures_for_delay} failures ({connection_error_delay}s / {scan_interval}s)")
        
        # Use persistent storage in hass.data - survives reloads
        storage_key = f"{name}_data_store"
        if storage_key not in hass.data:
            hass.data[storage_key] = {
                "setting_data": {},
                "realtime_data": {},
            }
        self.data_store = hass.data[storage_key]

        # Mark HA as not fully started yet
        self._ha_started = False
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, self._on_ha_started)

        try:
            self._client = ModbusTcpClient(host=host, port=port, timeout=60)
            _LOGGER.debug(f"Modbus client initialized for {host}:{port}")
        except Exception as e:
            _LOGGER.exception(f"Failed to initialize Modbus client: {e}")

    def _on_ha_started(self, event):
        """Callback fired when Home Assistant has fully started."""
        self._ha_started = True
        _LOGGER.debug("Home Assistant startup complete")

    @callback
    def async_remove_listener(self, update_callback: CALLBACK_TYPE) -> None:
        """Remove data update listener and close connection if no listeners remain."""
        super().async_remove_listener(update_callback)
        _LOGGER.debug("Removed update listener")

        # If no listeners remain, close the Modbus connection
        if not self._listeners:
            _LOGGER.debug("No listeners left, closing Modbus connection")
            try:
                self.close()
            except Exception as e:
                _LOGGER.exception(f"Error while closing the connection: {e}")

    def close(self) -> None:
        """Disconnect client."""
        try:
            with self._lock:
                if self._client is not None:
                    self._client.close()
                    self._client = None
            _LOGGER.debug("Modbus client connection closed")
        except Exception as e:
            _LOGGER.exception(f"Error closing Modbus connection: {e}")

    def _read_holding_registers(self, unit, address, count):
        """Safely read holding registers with reconnection logic."""
        # Block ALL reads during write flush
        if self._flush_running:
            _LOGGER.debug("Read skipped because write flush is running")
            return None
        
        try:
            # Ensure connection is alive
            if self._client is None or not self._client.connected:
                if not self._ha_started:
                    _LOGGER.debug("Modbus client not yet connected (HA still starting)")
                else:
                    _LOGGER.warning("Modbus client not connected, attempting reconnect...")

                # Close existing client if any
                if self._client is not None:
                    try:
                        self._client.close()
                    except Exception:
                        pass
                    self._client = None

                # Create new client
                try:
                    self._client = ModbusTcpClient(host=self._host, port=self._port, timeout=60)
                except Exception as e:
                    _LOGGER.exception(f"Failed to create new Modbus client: {e}")
                    return None

                if not self._client.connect():
                    _LOGGER.error("Modbus reconnect failed")
                    return None

            with self._modbus_lock:
                resp = self._client.read_holding_registers(
                    address=address,
                    count=count,
                    device_id=unit
                )

            # No response received
            if resp is None:
                _LOGGER.error(
                    f"Modbus returned no response for address {address}-{address+count-1}"
                )
                return None

            # Modbus returned an error frame
            if resp.isError():
                _LOGGER.error(
                    f"Modbus error reading registers {address}-{address+count-1}: {resp}"
                )
                # Force reconnect bij error frames - mogelijk gateway/warmtepomp communicatie probleem
                # Dit helpt wanneer de IP-gateway nog bereikbaar is maar niet met de warmtepomp kan communiceren
                _LOGGER.warning("Forcing reconnect due to Modbus error frame")
                if self._client is not None:
                    try:
                        self._client.close()
                    except Exception:
                        pass
                    self._client = None
                return None

            # Response object exists but contains no registers
            if not hasattr(resp, "registers"):
                _LOGGER.error(
                    f"Modbus response missing registers for {address}-{address+count-1}"
                )
                return None
            _LOGGER.debug( f"Successfully read {len(resp.registers)} registers from {address}-{address+count-1}" )
            
            # Update last successful read timestamp
            self._last_successful_read = datetime.now()
            
            return resp

        except (ConnectionException, ModbusIOException, ConnectionResetError, BrokenPipeError, OSError) as e:
            # Expected communication‑related errors
            _LOGGER.error(
                f"Modbus communication error while reading {address}-{address+count-1}: {e}"
            )
            # Mark client as disconnected to force reconnect on next attempt
            if self._client is not None:
                try:
                    self._client.close()
                except Exception:
                    pass
                self._client = None
            return None

        except Exception as e:
            # Unexpected internal errors (kept visible with full traceback)
            _LOGGER.exception(
                f"Unexpected error while reading registers {address}-{address+count-1}: {e}"
            )
            return None

    async def _async_update_data(self) -> dict:
        """Fetch Modbus data safely with clear logging and consistent return handling."""
        # Check if we haven't received valid data for too long (5 minutes)
        if self._last_successful_read is not None:
            time_since_success = (datetime.now() - self._last_successful_read).total_seconds()
            if time_since_success > 300:  # 5 minutes without successful reads
                _LOGGER.warning(
                    f"No successful reads for {int(time_since_success)}s (>5min), forcing reconnect"
                )
                if self._client is not None:
                    try:
                        self._client.close()
                    except Exception:
                        pass
                    self._client = None
        
        # Start with previous data - only overwrite if we get new data
        data: dict = {
            **self.data_store.get("setting_data", {}),
            **self.data_store.get("realtime_data", {}),
        }
        connection_status = "OK"
        failed_details = []

        # --- Read settings data ---
        settings_result = await self.hass.async_add_executor_job(self.read_modbus_setting_data)
        if isinstance(settings_result, tuple):
            settings, settings_failed_ranges = settings_result
        else:
            settings = settings_result
            settings_failed_ranges = []

        if settings is None:
            # Read skipped/failed (e.g. due to write flush) -> keep previous values
            _LOGGER.debug("Settings read failed or skipped, keeping previous values")
            settings = self.data_store.get("setting_data", {})
            connection_status = "Failed"
            failed_details.append("Settings read completely failed")
            settings_success = False
        elif settings == {}:
            _LOGGER.warning("Settings read returned empty data (decode error).")
            # Keep previous values instead of overwriting with empty
            settings = self.data_store.get("setting_data", {})
            connection_status = "Failed"
            failed_details.append("Settings decode error")
            settings_success = False
        else:
            # Check for partial failures
            if settings_failed_ranges:
                connection_status = "Partial"
                ranges_str = ','.join([f"{s}-{s+c-1}" for s, c in sorted(settings_failed_ranges)])
                failed_details.append(f"Settings ranges: {ranges_str}")
            settings_success = True

        data.update(settings)

        # --- Read realtime data ---
        realtime_result = await self.hass.async_add_executor_job(self.read_modbus_realtime_data)
        if isinstance(realtime_result, tuple):
            realtime, realtime_failed_ranges = realtime_result
        else:
            realtime = realtime_result
            realtime_failed_ranges = []

        if realtime is None:
            _LOGGER.debug("Realtime read failed or skipped, keeping previous values")
            realtime = self.data_store.get("realtime_data", {})
            connection_status = "Failed"
            failed_details.append("Realtime read completely failed")
            realtime_success = False
        elif realtime == {}:
            _LOGGER.warning("Realtime read returned empty data (decode error).")
            realtime = self.data_store.get("realtime_data", {})
            connection_status = "Failed"
            failed_details.append("Realtime decode error")
            realtime_success = False
        else:
            # Check for partial failures
            if realtime_failed_ranges:
                if connection_status == "OK":
                    connection_status = "Partial"
                ranges_str = ','.join([f"{s}-{s+c-1}" for s, c in sorted(realtime_failed_ranges)])
                failed_details.append(f"Realtime ranges: {ranges_str}")
            realtime_success = True

        data.update(realtime)

        # Store last known good data for next round (only if new data was successfully read)
        if settings_success:
            self.data_store["setting_data"] = settings
        if realtime_success:
            self.data_store["realtime_data"] = realtime

        # Set connection status
        if connection_status == "OK" and failed_details:
            connection_status = "Partial"
        data["connection_status"] = connection_status

        # Handle consecutive failures tracking
        if connection_status == "Failed":
            self._consecutive_failures += 1
            # Track when connection was first lost
            if self._consecutive_failures == 1:
                self._connection_lost_time = datetime.now()
            _LOGGER.debug(f"Consecutive failures: {self._consecutive_failures}/{self._failures_for_delay}, notified: {self._connection_error_notified}, mobile: {self._notify_connection_errors_mobile}, persistent: {self._notify_connection_errors_persistent}")
            
            # Send notification after configured delay of consecutive failures
            if self._consecutive_failures >= self._failures_for_delay and (self._notify_connection_errors_mobile or self._notify_connection_errors_persistent) and not self._connection_error_notified:
                # Format timestamp
                if self._connection_lost_time:
                    lost_time = self._connection_lost_time.strftime("%d-%m-%Y %H:%M:%S")
                else:
                    lost_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                
                message_nl = f"Communicatie met de Amber verloren sinds {lost_time}"
                message_en = f"Communication with the Amber lost since {lost_time}"
                
                _LOGGER.info(f"Sending connection error notification after {self._consecutive_failures} failures ({self._consecutive_failures * self.update_interval.total_seconds():.0f}s). notify_services: '{self._notify_services}'")
                
                # Send persistent notification if enabled
                if self._notify_connection_errors_persistent:
                    create_persistent_notification(
                        self.hass, 
                        message_nl, 
                        self._notification_title,
                        "itho_amber_connection_error"
                    )
                
                # Send to mobile apps if configured
                if self._notify_connection_errors_mobile and self._notify_services:
                    services = [s.strip() for s in self._notify_services.split(',') if s.strip()]
                    _LOGGER.info(f"Parsed notify services: {services}")
                    for service_name in services:
                        try:
                            await self.hass.services.async_call(
                                'notify',
                                service_name,
                                {'message': message_nl, 'title': self._notification_title}
                            )
                            _LOGGER.info(f"Connection error notification sent to {service_name}")
                        except Exception as notify_err:
                            _LOGGER.error(f"Failed to send notification to {service_name}: {notify_err}")
                else:
                    if self._notify_connection_errors_mobile:
                        _LOGGER.warning(f"No notify services configured for connection errors, skipping mobile notifications")
                
                self._connection_error_notified = True
                
        elif connection_status == "OK":
            # Reset failure counter on success
            if self._consecutive_failures > 0:
                _LOGGER.debug(f"Connection restored, resetting {self._consecutive_failures} consecutive failures")
            self._consecutive_failures = 0
            self._connection_lost_time = None  # Reset lost time
            # Only reset connection error flag when connection is restored
            self._connection_error_notified = False
            # Keep partial failure tracking to avoid re-notifying on same issues

                
        return data

    def read_modbus_setting_data(self) -> tuple[dict, int]:
        """Read all settings data."""
        ranges = [
            (0, 60), (60, 60), (120, 50), (170, 50),
            (314, 11), (334, 7), (375, 2), (407, 53)
        ]
        all_registers = []
        failed_ranges = []

        _LOGGER.debug("Start reading settings data")

        for start, count in ranges:
            success = False
            for attempt in range(MAX_READ_RETRIES):
                resp = self._read_holding_registers(unit=1, address=start, count=count)
                if resp is not None and not resp.isError() and hasattr(resp, "registers") and len(resp.registers) >= count:
                    all_registers.extend(resp.registers)
                    _LOGGER.debug(f"Read {len(resp.registers)} registers from {start}-{start+count-1} on attempt {attempt+1}")
                    success = True
                    break
                else:
                    _LOGGER.warning(f"Attempt {attempt+1} failed for range {start}-{start+count-1}")
                    time.sleep(0.5)  # Short delay between retries

            if not success:
                _LOGGER.error(f"Failed to read range {start}-{start+count-1} after {MAX_READ_RETRIES} attempts")
                failed_ranges.append((start, count))
                # Skip this range and continue with others

        if failed_ranges:
            _LOGGER.warning(f"Some ranges failed: {failed_ranges}. Proceeding with available data.")

        if not all_registers:
            _LOGGER.error("No settings data could be read")
            return None, failed_ranges

        _LOGGER.debug("Finished reading settings data")

        # --- Decode phase ---
        try:
            newdecoder = ModbusTcpClient.convert_from_registers(
                all_registers, data_type=ModbusTcpClient.DATATYPE.INT16
            )

            data = {}
            register_map = {}
            idx = 0

            # Build index map
            for start, count in ranges:
                if (start, count) not in failed_ranges:
                    for i in range(count):
                        reg = start + i
                        register_map[reg] = idx
                        idx += 1

            # Registers to skip (decoded separately)
            skip = {
                9, 18, 66, 71, 73, 119, 120, 121, 122,
                143, 144, 145, 146, 147, 148, 149, 150,
                218, 137, 202, 203, 126, 323, 324, 339
            }

            # Normal registers
            for reg, index in register_map.items():
                if reg not in skip and index < len(newdecoder):
                    data[str(reg)] = newdecoder[index]

            # Status registers with lookup tables
            STATUS_MAPS = {
                "ON_OFF_STATUS": [
                    9, 18, 66, 71, 73, 120, 121, 122,
                    143, 144, 145, 146, 147, 148, 149, 150,
                    218, 323, 324, 339
                ],
                "MODE_SIGNAL_TYPE": [119, 203],
                "PUMP_TYPE": [137],
                "MODE_SIGNAL_OUTPUT": [202],
                "DISPLAY_TIME": [126]
            }

            for category, regs in STATUS_MAPS.items():
                decode_dict = globals().get(category)
                for reg in regs:
                    if reg in register_map:
                        idx = register_map[reg]
                        val = newdecoder[idx]
                        data[str(reg)] = decode_dict[val] if decode_dict and val in decode_dict else val

            return data, failed_ranges

        except Exception as e:
            _LOGGER.exception(f"Unexpected error decoding settings data: {e}")
            return {}, failed_ranges

    def read_modbus_realtime_data(self) -> tuple[dict, int]:
        """Read realtime sensor values."""
        ranges = [
            (499, 48),
            (703, 13)
        ]
        all_registers = []
        failed_ranges = []

        _LOGGER.debug("Start reading realtime data")

        # --- Read all Modbus ranges ---
        for start, count in ranges:
            success = False
            for attempt in range(MAX_READ_RETRIES):
                resp = self._read_holding_registers(unit=1, address=start, count=count)
                if resp is not None and not resp.isError() and hasattr(resp, "registers") and len(resp.registers) >= count:
                    all_registers.extend(resp.registers)
                    _LOGGER.debug(f"Read {len(resp.registers)} registers from {start}-{start+count-1} on attempt {attempt+1}")
                    success = True
                    break
                else:
                    _LOGGER.warning(f"Attempt {attempt+1} failed for range {start}-{start+count-1}")
                    time.sleep(0.5)

            if not success:
                _LOGGER.error(f"Failed to read range {start}-{start+count-1} after {MAX_READ_RETRIES} attempts")
                failed_ranges.append((start, count))

        if failed_ranges:
            _LOGGER.warning(f"Some realtime ranges failed: {failed_ranges}. Proceeding with available data.")

        if not all_registers:
            _LOGGER.error("No realtime data could be read")
            return None, failed_ranges

        # --- Decode phase ---
        try:
            newdecoder = ModbusTcpClient.convert_from_registers(
                all_registers, data_type=ModbusTcpClient.DATATYPE.INT16
            )

            data = {}

            # Build index map
            register_map = {}
            idx = 0
            for start, count in ranges:
                if (start, count) not in failed_ranges:
                    for i in range(count):
                        reg = start + i
                        register_map[reg] = idx
                        idx += 1

            # --- Decode status bitfield (499) ---
            bit_messages = {
                0: "DHW Standby",
                1: "Heating Standby",
                2: "Cooling Standby",
                3: "DHW in progress",
                4: "Heating in progress",
                5: "Cooling in progress",
                6: "Timer in progress"
            }

            status_value = newdecoder[register_map[499]]
            status_text = self.get_highest_bit_message(status_value, bit_messages)
            data["499"] = status_text if status_text else ""

            # --- Decode realtime values ---
            realtime_keys = {
                501: (register_map[501], 0.01, "V{}-T{}"),
                502: (register_map[502], None, None),
                503: (register_map[503], None, None),
                504: (register_map[504], 0.01, "V{}"),
                505: (register_map[505], 0.1, None),
                506: (register_map[506], 0.1, None),
                507: (register_map[507], 0.1, None),
                508: (register_map[508], 0.1, None),
                509: (register_map[509], 0.1, None),
                510: (register_map[510], 0.1, None),
                511: (register_map[511], 0.1, None),
                512: (register_map[512], None, None),
                513: (register_map[513], None, None),
                515: (register_map[515], None, None),
                516: (register_map[516], None, None),
                517: (register_map[517], 0.1, None),
                518: (register_map[518], 0.1, None),
                519: (register_map[519], 0.1, None),
                520: (register_map[520], 0.1, None),
                521: (register_map[521], 0.1, None),
                522: (register_map[522], 0.1, None),
                523: (register_map[523], 0.1, None),
                524: (register_map[524], 0.1, None),
                525: (register_map[525], 0.1, None),
                526: (register_map[526], None, None),
                527: (register_map[527], None, None),
                528: (register_map[528], 0.1, None),
                529: (register_map[529], None, None),
                531: (register_map[531], 0.1, None),
                537: (register_map[537], 0.1, None),
                538: (register_map[538], 0.1, None),
                539: (register_map[539], 0.1, None),
                544: (register_map[544], None, None),
                545: (register_map[545], None, None),
                546: (register_map[546], None, None),
            }

            for key, (index, scale, fmt) in realtime_keys.items():
                if index < len(newdecoder):
                    val = newdecoder[index]

                    if scale:
                        val = round(val * scale, 2)

                    if fmt:
                        if key == 501:
                            t_raw = newdecoder[register_map[503]]
                            t = t_raw >> 5
                            data[str(key)] = fmt.format(str(val), t)
                        else:
                            data[str(key)] = fmt.format(val)
                    else:
                        data[str(key)] = val

            # --- delta-T ---
            deltaT = newdecoder[register_map[505]] - newdecoder[register_map[506]]
            data["delta-T"] = round(abs(deltaT) * 0.1, 2)

            # --- Status decoding ---
            status = {
                "ON_OFF_STATUS": {
                    "530": register_map[530], "532": register_map[532],
                    "533": register_map[533], "534": register_map[534],
                    "535": register_map[535], "536": register_map[536]
                },
                "CURRENT_OPERATION_MODE": {"514": register_map[514]},
                "LOGIN_STATUS": {"500": register_map[500]},
            }

            for category, statuses in status.items():
                decode_dict = globals().get(category)
                for key, index in statuses.items():
                    if index < len(newdecoder):
                        val = newdecoder[index]
                        if decode_dict and val in decode_dict:
                            data[key] = decode_dict[val]

            # --- Failure and active status bits ---
            status_bits = {
                "ACTIVE_STATUS": {
                    "P04": (register_map[499] + 41, 3),
                    "P07": (register_map[499] + 41, 6),
                    "P12": (register_map[499] + 41, 11),
                },
                "FAILURE_STATUS": {
                    "P01": (register_map[499] + 41, 0), "P02": (register_map[499] + 41, 1),
                    "P03": (register_map[499] + 41, 2), "P05": (register_map[499] + 41, 4),
                    "P06": (register_map[499] + 41, 5),
                    "P08": (register_map[499] + 41, 7), "P09": (register_map[499] + 41, 8),
                    "P10": (register_map[499] + 41, 9), "P11": (register_map[499] + 41, 10),
                    "P13": (register_map[499] + 41, 12),

                    "F01": (register_map[499] + 42, 5), "F02": (register_map[499] + 42, 6),
                    "F03": (register_map[499] + 42, 7), "F04": (register_map[499] + 42, 8),
                    "F05": (register_map[499] + 42, 9), "F06": (register_map[499] + 42, 10),
                    "F07": (register_map[499] + 42, 11), "F09": (register_map[499] + 42, 13),
                    "F10": (register_map[499] + 42, 14), "F11": (register_map[499] + 42, 15),

                    "F12": (register_map[499] + 43, 0), "F13": (register_map[499] + 43, 1),
                    "F14": (register_map[499] + 43, 2), "F15": (register_map[499] + 43, 3),
                    "F16": (register_map[499] + 43, 4), "F17": (register_map[499] + 43, 5),
                    "F18": (register_map[499] + 43, 6), "F21": (register_map[499] + 43, 7),
                    "F22": (register_map[499] + 43, 8), "F25": (register_map[499] + 43, 9),
                    "F27": (register_map[499] + 43, 10), "F28": (register_map[499] + 43, 11),
                    "F29": (register_map[499] + 43, 12), "F30": (register_map[499] + 43, 13),

                    "E01": (register_map[499] + 41, 13), "E02": (register_map[499] + 41, 14),
                    "E03": (register_map[499] + 41, 15), "E04": (register_map[499] + 42, 0),
                    "E05": (register_map[499] + 42, 1), "E06": (register_map[499] + 42, 2),
                    "E07": (register_map[499] + 42, 3), "E08": (register_map[499] + 42, 4),

                    "S01": (register_map[499] + 43, 14), "S02": (register_map[499] + 43, 15),
                    "S03": (register_map[499] + 44, 0),  "S04": (register_map[499] + 44, 1),
                    "S05": (register_map[499] + 44, 2),  "S06": (register_map[499] + 44, 3),
                    "S07": (register_map[499] + 44, 4),  "S08": (register_map[499] + 44, 5),
                    "S09": (register_map[499] + 44, 6),  "S10": (register_map[499] + 44, 7),
                    "S11": (register_map[499] + 44, 8),  "S13": (register_map[499] + 44, 9),
                }
            }

            for category, failures in status_bits.items():
                decode_dict = globals().get(category)
                for key, (index, shift) in failures.items():
                    if index < len(newdecoder):
                        val = (newdecoder[index] >> shift) & 1
                        if decode_dict and val in decode_dict:
                            data[key] = decode_dict[val]

            # --- Setpoints (703–715) ---
            setpoint_scales = {
                703: 0.1, 704: 0.1, 705: 1, 706: 1, 707: 1, 708: 1, 709: 1,
                710: 1, 711: 1, 712: 1, 713: 1, 714: 0.1, 715: 0.1
            }

            for reg, scale in setpoint_scales.items():
                if reg in register_map:
                    sp_idx = register_map[reg]
                    if sp_idx < len(newdecoder):
                        val = newdecoder[sp_idx]
                        data[str(reg)] = round(val * scale, 2)

            _LOGGER.debug(f"Finished reading realtime data")
            return data, failed_ranges

        except Exception as e:
            _LOGGER.exception(f"Unexpected error decoding realtime data: {e}")
            return {}, failed_ranges
    
    def get_highest_bit_message(self, register_value: int, bit_messages: dict) -> str:
        highest_bit = max((bit for bit in bit_messages if register_value & (1 << bit)), default=None)
        return bit_messages[highest_bit] if highest_bit is not None else ""

    def write_registers(self, address: int, value) -> None:
        """Queue register writes and coalesce them within 400ms."""
        try:
            # Normalize list payloads
            if isinstance(value, list):
                if len(value) == 1:
                    value = value[0]  # [31] → 31
                else:
                    # Multiple values → sequential writes
                    for i, v in enumerate(value):
                        self.write_registers(address + i, v)
                    return

            # Force to int (HA sometimes sends strings/floats)
            value = int(value)

            with self._lock:
                self._write_queue.append((address, value))

                if self._write_timer is not None:
                    self._write_timer.cancel()

                self._write_timer = threading.Timer(0.7, self._flush_write_queue)
                self._write_timer.start()

        except Exception as e:
            _LOGGER.exception(f"Unexpected error queuing write: {e}")

    def _flush_write_queue(self):
        """Write all queued registers sequentially, then refresh."""
        # If a flush is already running, mark that another flush is needed
        if self._flush_running:
            self._flush_pending = True
            _LOGGER.debug("Flush already running, marking pending flush")
            return

        self._flush_running = True

        try:
            while True:
                with self._lock:
                    # Deduplicate: last write per address wins
                    dedup = {}
                    for addr, val in self._write_queue:
                        dedup[addr] = val

                    writes = list(dedup.items())

                    self._write_queue = []
                    self._write_timer = None
                    self._flush_pending = False

                # No writes? Stop.
                if not writes:
                    break

                # Perform writes
                for address, value in writes:
                    with self._modbus_lock:
                        result = self._client.write_register(address, value, device_id=1)

                    if result.isError():
                        _LOGGER.error(f"Modbus write failed at address {address} with value {value}")
                        continue

                    _LOGGER.debug(f"Successfully wrote to register {address} with value {value}")
                    time.sleep(0.1)

                # Allow heat pump to process
                time.sleep(2)

                # Refresh HA
                self.hass.loop.call_soon_threadsafe(
                    lambda: asyncio.create_task(self.async_request_refresh())
                )
                self.hass.loop.call_soon_threadsafe(self._schedule_refresh)

                # If new writes arrived during flush, loop again
                if not self._flush_pending:
                    break

        except Exception as e:
            _LOGGER.exception(f"Unexpected error during write flush: {e}")

        finally:
            self._flush_running = False
  