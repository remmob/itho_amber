"""Itho Daalderop Amber 65/95/120 Modbus Hub/coordinator."""

import logging
import threading
import asyncio
import traceback
from datetime import timedelta

from voluptuous.validators import Number
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ConnectionException, ModbusIOException

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

        self._lock = threading.Lock()
        self._client = None
        self.data_store: dict[str, dict] = {
            "settings": {f"setting_data_{i}": {} for i in range(1, 7)},
            "realtime_data": {},
            "setpoint_data": {}
        }

        try:
            self._client = ModbusTcpClient(host=host, port=port, timeout=60)
        except Exception as e:
            _LOGGER.error(f"Error initializing Modbus client: {e}")

    @callback
    def async_remove_listener(self, update_callback: CALLBACK_TYPE) -> None:
        """Remove data update listener."""
        super().async_remove_listener(update_callback)

        # If no listeners are left, safely close the connection
        if not self._listeners:
            try:
                self.close()
            except Exception as e:
                _LOGGER.error(f"Error while closing the connection: {e}")

    def close(self) -> None:
        """Disconnect client."""
        try:
            with self._lock:
                self._client.close()
        except Exception as e:
            _LOGGER.error(f"Error closing connection: {e}")

    def _read_holding_registers(self, unit, address, count) -> None:
        """Read holding registers."""
        try:
            with self._lock:
                return self._client.read_holding_registers(address=address, count=count, device_id=unit)
        except Exception as e:
            _LOGGER.error(f"Error while reading registers: {e}")
            return None

    async def _async_update_data(self) -> dict:
        """Update Modbus data asynchronously."""
        
        data_sources = [
            self.read_modbus_setting_data_1,
            self.read_modbus_setting_data_2,
            self.read_modbus_setting_data_3,
            self.read_modbus_setting_data_4,
            self.read_modbus_setting_data_5,
            self.read_modbus_setting_data_6,
            self.read_modbus_realtime_data,
            self.read_modbus_setpoint_data
        ]

        data = {}

        try:
            results = await asyncio.gather(
                *(self.hass.async_add_executor_job(source) for source in data_sources),
                return_exceptions=True  # Prevent one failure is breaking
            )

            for source, result in zip(data_sources, results):
                if isinstance(result, Exception):
                    _LOGGER.error(f"Error fetching data from {source.__name__}: {result}")
                else:
                    data.update(result)

        except ConnectionException:
            _LOGGER.error("Reading Modbus data failed! Device is unreachable.")

        return data
    
    # settings data 1
    def read_modbus_setting_data_1(self) -> dict: #0 t/m 119
        """Read settings data 1"""
        setting_data_1 = self._read_holding_registers(unit=1, address=0, count=120)
        
        if setting_data_1.isError():
            _LOGGER.error("Failed to read Modbus registers for settings data")
            return {}

        data = {}

        try:
            # Ensure registers exist before converting
            if not hasattr(setting_data_1, "registers") or not isinstance(setting_data_1.registers, list) or len(setting_data_1.registers) < 120:
                _LOGGER.error("Error: The setpoint data, did not received enough registers!")
                return {}

            newdecoder = ModbusTcpClient.convert_from_registers(setting_data_1.registers, data_type=ModbusTcpClient.DATATYPE.INT16) 

            # Ensure decoded data has enough elements
            if len(newdecoder) < 120:
                _LOGGER.error("Error: Unexpected size of decoded data")
                return {}
            
            # Automatic calculation of register-index mapping
            register_map = {reg: reg - 0 for reg in [
                0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17,
                19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                34, 35, 36, 37, 38 , 39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
                49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63,
                64, 65, 67, 68, 69, 70, 72, 73, 74, 75, 76, 77, 78, 79, 80,
                81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95,
                96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108,
                109, 110, 111, 112, 113, 114, 115, 116, 117, 118
            ]}

            # Process each register
            for register, index in register_map.items():
                if index < len(newdecoder):
                    data[str(register)] = newdecoder[index]
                else:
                    _LOGGER.warning(f"Register {register} expects index {index}, but newdecoder has length {len(newdecoder)}")

            # define mapping for statuses
            status = {
                "ON_OFF_STATUS": { "9": 9, "18": 18, "66": 66, "71": 71, "73": 73,},
                "MODE_SIGNAL_TYPE": { "119": 119 }
            }

             # Loop through the dictionary to process statuses
            for category, statuses in status.items():
                for key, index in statuses.items():
                    value = newdecoder[index]
                    if value in globals()[category]:  
                        data[key] = globals()[category][value]

        except IndexError as e:
            _LOGGER.error(f"IndexError: {e}")
            return {}

        except Exception as e:
            _LOGGER.error(f"Unexpected Error: {e}\n{traceback.format_exc()}")
            return {}    

        return data

    # settings data 2
    def read_modbus_setting_data_2(self) -> dict: #120 t/m 219
        """Read settings data 2"""
        setting_data_2 = self._read_holding_registers(unit=1, address=120, count=100) 
        
        if setting_data_2.isError():
            _LOGGER.error("Failed to read Modbus registers for settings data")
            return {}

        data = {}

        try:
            # Ensure registers exist before converting
            if not hasattr(setting_data_2, "registers") or not isinstance(setting_data_2.registers, list) or len(setting_data_2.registers) < 100:

                _LOGGER.error("Error: The setpoint data, did not received enough registers!")
                return {}

            newdecoder = ModbusTcpClient.convert_from_registers(setting_data_2.registers, data_type=ModbusTcpClient.DATATYPE.INT16)

            # Ensure decoded data has enough elements
            if len(newdecoder) < 100:
                _LOGGER.error("Error: Unexpected size of decoded data")
                return {}

            # Automatic calculation of register-index mapping
            register_map = {reg: reg - 120 for reg in [
                123, 124, 125, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136,
                138, 139, 140, 141, 142, 151, 152, 153, 154, 155, 156, 157, 158, 
                159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 
                172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 
                185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 
                198, 199, 200, 201, 204, 205, 206, 207, 208, 209, 210, 211, 212,
                213, 214, 215, 216, 217, 219
            ]}

            # Process each register
            for register, index in register_map.items():
                if index < len(newdecoder):
                    data[str(register)] = newdecoder[index]
                else:
                    _LOGGER.warning(f"Register {register} expects index {index}, but newdecoder has length {len(newdecoder)}")

            # define mapping for statuses
            status = {
                "ON_OFF_STATUS": { "120": 0, "121": 1, "122": 2, "143": 23, "144": 24, "145": 25, "146": 26, "147": 27, 
                    "148": 28, "149": 29, "150": 30, "218": 98 },
                "PUMP_TYPE": { "137": 17 },	
                "MODE_SIGNAL_OUTPUT": { "202": 82 },	
                "MODE_SIGNAL_TYPE": { "203": 83 },	
                "DISPLAY_TIME": { "126": 6 }
            }
        
            # Loop through the dictionary to process statuses
            for category, statuses in status.items():
                for key, index in statuses.items():
                    value = newdecoder[index]
                    if value in globals()[category]:  
                        data[key] = globals()[category][value]


        except IndexError as e:
            _LOGGER.error(f"IndexError: {e}")
            return {}

        except Exception as e:
            _LOGGER.error(f"Unexpected Error: {e}\n{traceback.format_exc()}")
            return {}

        return data

    # settings data 3
    def read_modbus_setting_data_3(self) -> dict: #314 t/m 324
        """Read settings data 3"""
        setting_data_3 = self._read_holding_registers(unit=1, address=314, count=11)
        
        if setting_data_3.isError():
            _LOGGER.error("Failed to read Modbus registers for settings data")
            return {}

        data = {}

        try:
            # Ensure registers exist before converting
            if not hasattr(setting_data_3, "registers") or not isinstance(setting_data_3.registers, list) or len(setting_data_3.registers) < 11:
                _LOGGER.error("Error: The setpoint data, did not received enough registers!")
                return {}

            newdecoder = ModbusTcpClient.convert_from_registers(setting_data_3.registers, data_type=ModbusTcpClient.DATATYPE.INT16)

            # Ensure decoded data has enough elements
            if len(newdecoder) < 11:
                _LOGGER.error("Error: Unexpected size of decoded data")
                return {}
            
            # Map decoded values
            register_map = {reg: reg - 314 for reg in [314, 315, 316, 317, 318, 319, 320, 321, 322 ]}

            # Process each register
            for register, index in register_map.items():
                if index < len(newdecoder):
                    data[str(register)] = newdecoder[index]
                else:
                    _LOGGER.warning(f"Register {register} expects index {index}, but newdecoder has length {len(newdecoder)}")

            S323 = newdecoder[9]
            if S323 in ON_OFF_STATUS:
                data ["323"] = ON_OFF_STATUS[S323]

            S324= newdecoder[10]
            if S324 in ON_OFF_STATUS:
                data ["324"] = ON_OFF_STATUS[S324]    

        except IndexError as e:
            _LOGGER.error(f"IndexError: {e}")
            return {}

        except Exception as e:
            _LOGGER.error(f"Unexpected Error: {e}\n{traceback.format_exc()}")
            return {}
 
        return data
    
    # Settings data 4
    def read_modbus_setting_data_4(self) -> dict: #334 & 340
        """Read settings data 4"""
        setting_data_4 = self._read_holding_registers(unit=1, address=334, count=7)
        
        if setting_data_4.isError():
            _LOGGER.error("Failed to read Modbus registers for settings data")
            return {}

        data = {}

        try:
            # Ensure registers exist before converting
            if not hasattr(setting_data_4, "registers") or not isinstance(setting_data_4.registers, list) or len(setting_data_4.registers) < 7:
                _LOGGER.error("Error: The setpoint data, did not received enough registers!")
                return {}
                
            newdecoder = ModbusTcpClient.convert_from_registers(setting_data_4.registers, data_type=ModbusTcpClient.DATATYPE.INT16)
            
            # Ensure decoded data has enough elements
            if len(newdecoder) < 7:
                _LOGGER.error("Error: Unexpected size of decoded data")
                return {}
            
            # Map decoded values
            register_map = {reg: reg - 334 for reg in  [334, 335, 336, 337, 338, 340 ]}

            # Process each register
            for register, index in register_map.items():
                if index < len(newdecoder):
                    data[str(register)] = newdecoder[index]
                else:
                    _LOGGER.warning(f"Register {register} expects index {index}, but newdecoder has length {len(newdecoder)}")

            S339 = newdecoder[5] 
            if S339 in ON_OFF_STATUS: data ["339"] = ON_OFF_STATUS[S339]
        
        except IndexError as e:
            _LOGGER.error(f"IndexError: {e}")
            return {}

        except Exception as e:
            _LOGGER.error(f"Unexpected Error: {e}\n{traceback.format_exc()}")
            return {}

        return data

    # Settings data 5
    def read_modbus_setting_data_5(self) -> dict: #375 & 376
        """Read settings data 5"""
        setting_data_5 = self._read_holding_registers(unit=1, address=375, count=2)
        
        if setting_data_5.isError():
            _LOGGER.error("Failed to read Modbus registers for settings data")
            return {}

        data = {}

        try:
            # Ensure registers exist before converting
            if not hasattr(setting_data_5, "registers") or not isinstance(setting_data_5.registers, list) or len(setting_data_5.registers) < 2:
                _LOGGER.error("Error: The setpoint data, did not received enough registers!")
                return {}

            newdecoder = ModbusTcpClient.convert_from_registers(setting_data_5.registers, data_type=ModbusTcpClient.DATATYPE.INT16)

            # Ensure decoded data has enough elements
            if len(newdecoder) < 2:
                _LOGGER.error("Error: Unexpected size of decoded data")
                return {}
            
            # Map decoded values
            register_map = {reg: reg - 375 for reg in [375, 376 ]}

            # Process each register
            for register, index in register_map.items():
                if index < len(newdecoder):
                    data[str(register)] = newdecoder[index]
                else:
                    _LOGGER.warning(f"Register {register} expects index {index}, but newdecoder has length {len(newdecoder)}")

        except IndexError as e:
            _LOGGER.error(f"IndexError: {e}")
            return {}

        except Exception as e:
            _LOGGER.error(f"Unexpected Error: {e}\n{traceback.format_exc()}")
            return {}

        return data

    # Settings data 6
    def read_modbus_setting_data_6(self) -> dict: #407 t/m 459
        """Read settings data 6"""
        setting_data_6 = self._read_holding_registers(unit=1, address=407, count=53)

        if setting_data_6.isError():
            _LOGGER.error("Failed to read Modbus registers for settings data")
            return {}
        
        data = {}
        
        try:
            # Ensure registers exist before converting
            if not hasattr(setting_data_6, "registers") or not isinstance(setting_data_6.registers, list) or len(setting_data_6.registers) < 53:
                _LOGGER.error("Error: The setpoint data, did not received enough registers!")
                return {}

            newdecoder = ModbusTcpClient.convert_from_registers(setting_data_6.registers, data_type=ModbusTcpClient.DATATYPE.INT16)

            # Ensure decoded data has enough elements
            if len(newdecoder) < 53:
                _LOGGER.error("Error: Unexpected size of decoded data")
                return {}

            # Map decoded values
            register_map = {reg: reg - 407 for reg in [
                407, 408, 409, 410, 411, 412, 413, 414,
                415, 416, 417, 418, 419, 420, 421, 422,
                423, 424, 425, 426, 427, 428, 429, 430,
                431, 432, 433, 434, 435, 436, 437, 438,
                439, 440, 441, 442, 443, 444, 445, 446,
                447, 448, 449, 450, 451, 452, 453, 454,
                455, 456, 457, 458, 459
            ]}

            # Process each register
            for register, index in register_map.items():
                if index < len(newdecoder):
                    data[str(register)] = newdecoder[index]
                else:
                    _LOGGER.warning(f"Register {register} expects index {index}, but newdecoder has length {len(newdecoder)}")

        except IndexError as e:
            _LOGGER.error(f"IndexError: {e}")
            return {}

        except Exception as e:
            _LOGGER.error(f"Unexpected Error: {e}\n{traceback.format_exc()}")
            return {}

        return data

    # Realtime data
    def read_modbus_realtime_data(self) -> dict: # 499 t/m 539
        """Read the reatime sensor values"""
        realtime_data = self._read_holding_registers(unit=1, address=499, count=48)

        if realtime_data.isError():
            _LOGGER.error("Failed to read Modbus registers for realtime data")
            return {}

        data = {}

        try:
            # Ensure registers exist before converting
            if not hasattr(realtime_data, "registers") or not isinstance(realtime_data.registers, list) or len(realtime_data.registers) < 48:
                _LOGGER.error("Error: The setpoint data, did not received enough registers!")
                return {}
        
            newdecoder = ModbusTcpClient.convert_from_registers(realtime_data.registers, data_type=ModbusTcpClient.DATATYPE.INT16)

            # Ensure decoded data has enough elements
            if len(newdecoder) < 48:
                _LOGGER.error("Error: Unexpected size of decoded data")
                return {}

            # Check wich bit is active and return the current working mode
            # bit messages
            bit_messages = {
                0: "DHW Standby",
                1: "Heating Standby",
                2: "Cooling Standby",
                3: "DHW in progress",
                4: "Heating in progress",
                5: "Cooling in progress",
                6: "Timer in progress"
            }
            
            #modbus_register = newdecoder[0]
            resultaat = self.get_highest_bit_message(newdecoder[0], bit_messages)

            if resultaat:
                data["499"] = resultaat
            else:   
                data["499"] = ""

            # Define register mapping and scaling
            register_keys = {
                501: (2, 0.01, "V{}-T{}"), 502: (3, None, None),
                503: (4, 0.01, "V{}"), 504: (5, 0.01, "V{}"),
                505: (6, 0.1, None), 506: (7, 0.1, None),
                507: (8, 0.1, None), 508: (9, 0.1, None),
                509: (10, 0.1, None), 510: (11, 0.1, None),
                511: (12, 0.1, None), 512: (13, None, None),
                513: (14, None, None), 515: (16, None, None),
                516: (17, None, None), 517: (18, 0.1, None),
                518: (19, 0.1, None), 519: (20, 0.1, None),
                520: (21, 0.1, None), 521: (22, 0.1, None),
                522: (23, 0.1, None), 523: (24, 0.1, None),
                524: (25, 0.1, None), 525: (26, 0.1, None),
                526: (27, None, None), 527: (28, None, None),
                528: (29, 0.1, None), 529: (30, None, None),
                531: (32, 0.1, None), 537: (38, 0.1, None),
                538: (39, 0.1, None), 539: (40, 0.1, None),
                544: (45, None, None), 545: (46, None, None),
                546: (47, None, None)
            }

            # Process each register
            for key, (index, scale, format_str) in register_keys.items():
                value = newdecoder[index]

                if scale:
                    value = round(value * scale, 2)

                if format_str:
                    if key == 501:  # Special formatting for key 501
                        versionleft = str(value)
                        data[str(key)] = format_str.format(versionleft, newdecoder[3])
                    else:
                        data[str(key)] = format_str.format(value)
                else:
                    data[str(key)] = value

            # Compute `delta-T`
            deltaT = newdecoder[6] - newdecoder[7]
            data["delta-T"] = round(abs(deltaT) * 0.1, 2)

            # define mapping for statuses
            status = {
                "ON_OFF_STATUS": { "530":31, "532":33, "533":34, "534":35, "535":36, "536":37 },
                "CURRENT_OPERATION_MODE": { "514":15 },
                "LOGIN_STATUS": { "500":1 }
            }

            # Loop through the dictionary to process statuses
            for category, statuses in status.items():
                for key, index in statuses.items():
                    value = newdecoder[index]
                    if value in globals()[category]:  
                        data[key] = globals()[category][value]

            # Define the bit positions for each category
            status_bits = {
                "FAILURE_STATUS": {
                    "P01": (41, 0), "P02": (41, 1), "P03": (41, 2), "P05": (41, 4), "P06": (41, 5),
                    "P08": (41, 7), "P09": (41, 8), "P10": (41, 9), "P11": (41, 10), "P13": (41, 12),
                    "F01": (42, 5), "F02": (42, 6), "F03": (42, 7), "F04": (42, 8), "F05": (42, 9),
                    "F06": (42, 10), "F07": (42, 11), "F09": (42, 13), "F10": (42, 14), "F11": (42, 15),
                    "F12": (43, 0), "F13": (43, 1), "F14": (43, 2), "F15": (43, 3), "F16": (43, 4),
                    "F17": (43, 5), "F18": (43, 6), "F21": (43, 7), "F22": (43, 8), "F25": (43, 9),
                    "F27": (43, 10), "F28": (43, 11), "F29": (43, 12), "F30": (43, 13),
                    "E01": (41, 13), "E02": (41, 14), "E03": (41, 15), "E04": (42, 0), "E05": (42, 1),
                    "E06": (42, 2), "E07": (42, 3), "E08": (42, 4),
                    "S01": (43, 14), "S02": (43, 15), "S03": (44, 0), "S04": (44, 1), "S05": (44, 2),
                    "S06": (44, 3), "S07": (44, 4), "S08": (44, 5), "S09": (44, 6), "S10": (44, 7),
                    "S11": (44, 8), "S13": (44, 9)
                },
                "ACTIVE_STATUS": {
                    "P04": (41, 3), "P07": (41, 6), "P12": (41, 11)
                }
            }

            # Loop through each category and process statuses
            for category, failures in status_bits.items():
                for key, (index, shift) in failures.items():
                    value = (newdecoder[index] >> shift) & 1
                    if value in globals()[category]:  # Dynamically access FAILURE_STATUS or ACTIVE_STATUS
                        data[key] = globals()[category][value]


        except IndexError as e:
            _LOGGER.error(f"IndexError: {e}")
            return {}

        except Exception as e:
            _LOGGER.error(f"Unexpected Error: {e}\n{traceback.format_exc()}")
            return {}

        return data

    # Setpoint data
    def read_modbus_setpoint_data(self) -> dict: # 703 t/m 715
        """Read the realtime setpoint values"""
        
        setpoint_data = self._read_holding_registers(unit=1, address=703, count=13)
        
        if setpoint_data.isError():
            _LOGGER.error("Failed to read Modbus registers for setpoint data")
            return {}

        data = {}

        try:
            # Ensure registers exist before converting
            if not hasattr(setpoint_data, "registers") or not isinstance(setpoint_data.registers, list) or len(setpoint_data.registers) < 13:
                _LOGGER.error("Error: The setpoint data, did not received enough registers!")
                return {}

            newdecoder = ModbusTcpClient.convert_from_registers(setpoint_data.registers, data_type=ModbusTcpClient.DATATYPE.INT16)

            # Ensure decoded data has enough elements
            if len(newdecoder) < 13:
                _LOGGER.error("Error: Unexpected size of decoded data")
                return {}

            # Map decoded values
            register_map = {
                703: 0.1, 704: 0.1, 705: 1, 706: 1, 707: 1, 708: 1, 709: 1, 710: 1,
                711: 1, 712: 1, 713: 1, 714: 0.1, 715: 0.1}

            # Process each register
            for i, (key, scale) in enumerate(register_map.items()):
                value = newdecoder[i]
                data[str(key)] = round(value * scale, 2)

        except IndexError as e:
            _LOGGER.error(f"IndexError: {e}")
            return {}

        except Exception as e:
            _LOGGER.error(f"Unexpected Error: {e}\n{traceback.format_exc()}")
            return {}

        return data

    # get highest bit
    def get_highest_bit_message(self, register_value: int, bit_messages: dict) -> str:
        highest_bit = max((bit for bit in bit_messages if register_value & (1 << bit)), default=None)
        return bit_messages[highest_bit] if highest_bit is not None else ""
     
    # write registers
    def write_registers(self, address: int, payload: list[int] | int) -> None:
        """Write register values safely."""
        try:
            with self._lock:
                result = self._client.write_registers(address, payload, device_id=1)
                if result.isError():
                    _LOGGER.error(f"Modbus write failed at address {address} with payload {payload}")
                else:
                    _LOGGER.info(f"Successfully wrote to register {address} with payload {payload}")
        except Exception as e:
            _LOGGER.error(f"Error writing to register {address}: {e}") 