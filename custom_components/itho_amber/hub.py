"""Itho Daalderop Amber 65/95/120 Modbus Hub/coordinator."""

import time
import logging
import threading
import asyncio
import traceback
from datetime import timedelta

from voluptuous.validators import Number
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ConnectionException, ModbusIOException
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import CALLBACK_TYPE, callback, HomeAssistant

from .const import (
    DOMAIN, LOGIN_STATUS, ON_OFF_STATUS, PUMP_TYPE, CURRENT_OPERATION_MODE,
    EXTERNAL_CONTROL, HWTBH_PRIORITY_MODE, MODE_SIGNAL_TYPE, MODE_SIGNAL_OUTPUT,
    DISPLAY_TIME, FAILURE_STATUS, ACTIVE_STATUS)

_LOGGER = logging.getLogger(__name__)

class AmberModbusHub(DataUpdateCoordinator[dict]):
    """Thread safe wrapper class for pymodbus."""

    def __init__(self, hass: HomeAssistant, name: str, host: str, port: int | float, scan_interval: int | float):
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
        self.data_store: dict[str, dict] = {
            "setting_data": {},
            "realtime_data": {},
        }

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
                self._client.close()
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
            if not self._client.connected:
                if not self._ha_started:
                    _LOGGER.debug("Modbus client not yet connected (HA still starting)")
                else:
                    _LOGGER.warning("Modbus client not connected, attempting reconnect...")

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
                return None

            # Response object exists but contains no registers
            if not hasattr(resp, "registers"):
                _LOGGER.error(
                    f"Modbus response missing registers for {address}-{address+count-1}"
                )
                return None
            _LOGGER.debug( f"Successfully read {len(resp.registers)} registers from {address}-{address+count-1}" )
            return resp

        except (ConnectionException, ModbusIOException) as e:
            # Expected communication‑related errors
            _LOGGER.error(
                f"Modbus communication error while reading {address}-{address+count-1}: {e}"
            )
            return None

        except Exception as e:
            # Unexpected internal errors (kept visible with full traceback)
            _LOGGER.exception(
                f"Unexpected error while reading registers {address}-{address+count-1}: {e}"
            )
            return None

    async def _async_update_data(self) -> dict:
        """Fetch Modbus data safely with clear logging and consistent return handling."""
        data: dict = {}

        try:
            # --- Read settings data ---
            settings = await self.hass.async_add_executor_job(self.read_modbus_setting_data)

            if settings is None:
                # Read skipped/failed (e.g. due to write flush) -> keep previous values
                _LOGGER.debug("Settings read failed or skipped, keeping previous values")
                settings = self.data_store.get("setting_data", {})
            elif settings == {}:
                _LOGGER.warning("Settings read returned empty data (decode error).")
                # Keep previous values instead of overwriting with empty
                settings = self.data_store.get("setting_data", {})

            data.update(settings)

            # --- Read realtime data ---
            realtime = await self.hass.async_add_executor_job(self.read_modbus_realtime_data)

            if realtime is None:
                _LOGGER.debug("Realtime read failed or skipped, keeping previous values")
                realtime = self.data_store.get("realtime_data", {})
            elif realtime == {}:
                _LOGGER.warning("Realtime read returned empty data (decode error).")
                realtime = self.data_store.get("realtime_data", {})

            data.update(realtime)

            # Store last known good data for next round
            self.data_store["setting_data"] = settings
            self.data_store["realtime_data"] = realtime

            return data

        except (ConnectionException, ModbusIOException) as e:
            _LOGGER.error(f"Modbus communication error during update: {e}")
            # On hard comms error also keep previous values
            return {
                **self.data_store.get("setting_data", {}),
                **self.data_store.get("realtime_data", {}),
            }

        except Exception as e:
            _LOGGER.exception(f"Unexpected error fetching Amber data: {e}")
            return {
                **self.data_store.get("setting_data", {}),
                **self.data_store.get("realtime_data", {}),
            }

    def read_modbus_setting_data(self) -> dict:
        """Read all settings data."""
        ranges = [
            (0, 60), (60, 60), (120, 50), (170, 50),
            (314, 11), (334, 7), (375, 2), (407, 53)
        ]
        all_registers = []

        _LOGGER.debug("Start reading settings data")

        for start, count in ranges:
            resp = self._read_holding_registers(unit=1, address=start, count=count)

            # Communication or Modbus error
            if resp is None:
                _LOGGER.debug(
                    f"Settings read failed for range {start}-{start+count-1} "
                    f"(communication issue or simultaneous write). Keeping previous values."
                )
                return None

            # Modbus error frame or missing registers
            if resp.isError() or not hasattr(resp, "registers"):
                _LOGGER.error(
                    f"Failed to read Modbus registers {start}-{start+count-1}"
                )
                return None

            # Incomplete read
            if len(resp.registers) < count:
                _LOGGER.warning(
                    f"Incomplete settings read: expected {count} registers, "
                    f"got {len(resp.registers)} for range {start}-{start+count-1}. "
                    f"Keeping previous values."
                )
                return None

            _LOGGER.debug(
                f"Read {len(resp.registers)} of {count} registers from {start}-{start+count-1}"
            )

            all_registers.extend(resp.registers)
            time.sleep(0.2)

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
                    idx = register_map[reg]
                    val = newdecoder[idx]
                    data[str(reg)] = decode_dict[val] if decode_dict and val in decode_dict else val

            return data

        except Exception as e:
            _LOGGER.exception(f"Unexpected error decoding settings data: {e}")
            return {}

    def read_modbus_realtime_data(self) -> dict:
        """Read realtime sensor values."""
        ranges = [
            (499, 48),
            (703, 13)
        ]
        all_registers = []

        _LOGGER.debug("Start reading realtime data")

        # --- Read all Modbus ranges ---
        for start, count in ranges:
            resp = self._read_holding_registers(unit=1, address=start, count=count)

            # 1) No response (resp is None) -> likely communication issue
            if resp is None:
                _LOGGER.debug(
                    f"Realtime data read failed for range {start}-{start+count-1} "
                    f"(communication issue or simultaneous write). Keeping previous values."
                )
                return None

            # 2) Modbus error frame
            if resp.isError():
                _LOGGER.error(
                    f"Modbus error reading registers {start}-{start+count-1}: {resp}"
                )
                return None

            # 3) Response without 'registers' attribute
            if not hasattr(resp, "registers"):
                _LOGGER.error(
                    f"Modbus response missing registers for {start}-{start+count-1}"
                )
                return None

            # 4) Incomplete read
            if len(resp.registers) < count:
                _LOGGER.warning(
                    f"Incomplete realtime read: expected {count} registers, "
                    f"got {len(resp.registers)} for range {start}-{start+count-1}. "
                    f"Keeping previous values."
                )
                return None

            _LOGGER.debug(
                f"Read {len(resp.registers)} of {count} registers from {start}-{start+count-1}"
            )

            all_registers.extend(resp.registers)
            time.sleep(0.1)

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
                for i in range(count):
                    reg = start + i
                    register_map[reg] = idx
                    idx += 1

            # _LOGGER.debug(
            #     f"Realtime: built register_map with {len(register_map)} entries, "
            #     f"decoder length={len(newdecoder)}"
            # )

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
                    val = (newdecoder[index] >> shift) & 1
                    if decode_dict and val in decode_dict:
                        data[key] = decode_dict[val]

            # --- Setpoints (703–715) ---
            setpoint_scales = {
                703: 0.1, 704: 0.1, 705: 1, 706: 1, 707: 1, 708: 1, 709: 1,
                710: 1, 711: 1, 712: 1, 713: 1, 714: 0.1, 715: 0.1
            }

            for reg, scale in setpoint_scales.items():
                sp_idx = register_map[reg]
                val = newdecoder[sp_idx]
                data[str(reg)] = round(val * scale, 2)

            _LOGGER.debug(f"Finished reading realtime data")
            return data

        except Exception as e:
            _LOGGER.exception(f"Unexpected error decoding realtime data: {e}")
            return {}
    
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

    # def write_registers(self, address: int, payload: list[int] | int) -> None:
    #     """Write register values safely and trigger refresh."""
    #     try:
    #         with self._lock:
    #             result = self._client.write_registers(address, payload, device_id=1)

    #         # Modbus returned an error frame
    #         if result.isError():
    #             _LOGGER.error(
    #                 f"Modbus write failed at address {address} with payload {payload}"
    #             )
    #             return

    #         # Successful write
    #         _LOGGER.debug(
    #             f"Successfully wrote to register {address} with payload {payload}"
    #         )

    #         # Allow device to process the write
    #         time.sleep(2)

    #         # Trigger Home Assistant refresh
    #         self.hass.loop.call_soon_threadsafe(
    #             lambda: asyncio.create_task(self.async_request_refresh())
    #         )
    #         self.hass.loop.call_soon_threadsafe(self._schedule_refresh)

    #     except Exception as e:
    #         _LOGGER.exception(
    #             f"Unexpected error writing to register {address}: {e}"
    #         )
  