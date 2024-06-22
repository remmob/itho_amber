"""Itho Daalderop Amber Modbus Hub."""

import logging
import threading
from datetime import timedelta
from voluptuous.validators import Number

from pymodbus.register_read_message import ReadHoldingRegistersResponse
from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.exceptions import ConnectionException
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.core import CALLBACK_TYPE, callback

from .const import (
    DOMAIN,
    CURRENT_MODE,
    LOGIN_STATUS,
    ON_OFF_STATUS,
    CURRENT_OPERATION_MODE,
    EXTERNAL_CONTROL,
    HWTBH_PRIORITY_MODE,
)

_LOGGER = logging.getLogger(__name__)

class AmberModbusHub(DataUpdateCoordinator[dict]):
    """Thread safe wrapper class for pymodbus."""

    def __init__(self, hass: HomeAssistantType, name: str, host: str, port: Number, scan_interval: Number):
        """Initialize the Itho Daalderop Amber Modbus hub."""
        super().__init__(hass, _LOGGER, name=name, update_interval=timedelta(seconds=scan_interval))

        self._client = ModbusTcpClient(host=host, port=port, timeout=5)
        self._lock = threading.Lock()

        self.settings_data: dict ={}
        self.realtime_data: dict = {}
        self.version_data: dict = {}
        
    @callback
    def async_remove_listener(self, update_callback: CALLBACK_TYPE) -> None:
        """Remove data update listener."""
        super().async_remove_listener(update_callback)

        """No listeners left then close connection"""
        if not self._listeners:
            self.close()

    def close(self) -> None:
        """Disconnect client."""
        with self._lock:
            self._client.close()

    def _read_holding_registers(self, unit, address, count) -> ReadHoldingRegistersResponse:
        """Read holding registers."""
        with self._lock:
            return self._client.read_holding_registers(address=address, count=count, slave=unit)  
    
    async def _async_update_data(self) -> dict:

        realtime_data = {}
        settings_data = {}
        version_info = {}

        try:
            """Read version info"""
            #version_info = await self.hass.async_add_executor_job(
            #       self.read_modbus_version_data)

            """Read settings info"""
            settings_data = await self.hass.async_add_executor_job(
                   self.read_modbus_settings_data)

            """Read realtime data"""
            realtime_data = await self.hass.async_add_executor_job(
                self.read_modbus_realtime_data)

        except ConnectionException:
            _LOGGER.error("Reading realtime data failed! the Amber is unreachable.")

        return {**realtime_data, **settings_data, **version_info}

 
 
    def read_modbus_version_data(self) -> dict:

        addresses = [501,502,503,504] #15 used of 125
        values = []
        data = {}
        try:
            for address in addresses:
                version_info = self._read_holding_registers(unit=1, address=address, count=1)
                decoder = BinaryPayloadDecoder.fromRegisters(settings_data.registers, byteorder=Endian.BIG)   
                value = decoder.decode_16bit_int()
                values.append(int(value))
        except:
            _LOGGER.error ("Error reading and decoding version data.")
        try:
            for key in addresses:
                for value in values:
                    data[str(key)] = value
                    values.remove(value)
                    break
        except:
            _LOGGER.error("Error creating version dictonary") 
        return data



    def read_modbus_settings_data(self) -> dict:
        #Read only the not writeable settings.
        addresses = [5,6,7,10,11,12,26,27,28 ,29,31,32,33,34,35,36,37,38,39 ,40,41,42,43,44,45,46,47,49,50 ,51,52,53,54,59,61,62,63,64,65 #40 
                    ,67,68,69,70,72,74,75,90,91,93 ,94,95,96,97,98,99,100,101,102,110 ,111,133,217,314,315,316,317,318,319,320 ,321,322] #71 used of 125
        values = []
        data = {}
        try:
            for address in addresses:
                settings_data = self._read_holding_registers(unit=1, address=address, count=1)
                decoder = BinaryPayloadDecoder.fromRegisters(settings_data.registers, byteorder=Endian.BIG)   
                value = decoder.decode_16bit_int()
                values.append(int(value))
        except:
            _LOGGER.error ("Error reading and decoding settings data.")
        try:
            for key in addresses:
                for value in values:
                    data[str(key)] = value
                    values.remove(value)
                    break
        except:
            _LOGGER.error("Error creating settings dictonary") 
        return data 


    def read_modbus_realtime_data(self) -> dict:

        addresses = [500,501,503,504,505,506,507,508,509,510, 511,514,515,516,517,518,519,520,521,522 ,523,524,525, #23
                     526,528,529,530,531,532,533,534,535,536, 537,538,539,92,30,499,8,3,219,143 ,323,144,324,66,71,135, #26
                     72,73,18,9,60,218] #55 used of 125
        values = []
        data =  {}
        try:
            for address in addresses:
                realtime_data = self._read_holding_registers(unit=1, address=address, count=1)
                decoder = BinaryPayloadDecoder.fromRegisters(realtime_data.registers, byteorder=Endian.BIG)
                value = decoder.decode_16bit_int()
                values.append(value)
        except:
            _LOGGER.error("Error reading and decoding realtime data")
     
        mode = values[38]
        _mode =[]
        _mode.extend(
            self.translate_mode_code_to_messages(mode, CURRENT_MODE.items()))
        data["499"] = ", ".join(_mode).strip()[0:254]

        if values[0] in LOGIN_STATUS:
            data["500"] = LOGIN_STATUS[values[0]]

        data["501"] = round(values[1] * 0.01,2)
        data["503"] = round(values[2] * 0.01, 2)
        data["504"] = round(values[3] * 0.01, 2)
        data["505"] = round(values[4] * 0.1, 2)
        data["506"] = round(values[5] * 0.1, 2)
        data["507"] = round(values[6] * 0.1, 2)
        data["508"] = round(values[7] * 0.1, 2)
        data["509"] = round(values[8] * 0.1, 2)
        data["510"] = round(values[9] * 0.1, 2)
        data["511"] = round(values[10] * 0.1, 2) 

        if values[11] in CURRENT_OPERATION_MODE:
            data["514"] = CURRENT_OPERATION_MODE[values[11]]

        data["515"] = values[12]
        data["516"] = values[13]
        data["517"] = round(values[14] * 0.1, 2)
        data["518"] = round(values[15] * 0.1, 2)
        data["519"] = round(values[16] * 0.1, 2)
        data["520"] = round(values[17] * 0.1, 2)
        data["521"] = round(values[18] * 0.1, 2)
        data["522"] = round(values[19] * 0.1, 2)
        data["523"] = round(values[20] * 0.1, 2)
        data["524"] = round(values[21] * 0.1, 2)
        data["525"] = round(values[22] * 0.1, 2)
        data["526"] = values[23]
        data["528"] = round(values[24] * 0.1, 2)
        data["529"] = values[25]

        if values[26] in ON_OFF_STATUS:
            data["530"] = ON_OFF_STATUS[values[26]]

        data["531"] = round(values[27] * 0.1, 2)

        if values[28] in ON_OFF_STATUS:
            data["532"] = ON_OFF_STATUS[values[28]]

        if values[29] in ON_OFF_STATUS:
            data["533"] = ON_OFF_STATUS[values[29]]
        
        if values[30] in ON_OFF_STATUS:
            data["534"] = ON_OFF_STATUS[values[30]]

        if values[31] in ON_OFF_STATUS:
            data["535"] = ON_OFF_STATUS[values[31]]

        if values[32] in ON_OFF_STATUS:
            data["536"] = ON_OFF_STATUS[values[32]] 

        data["537"] = round(values[33] * 0.1)
        data["538"] = round(values[34] * 0.1, 2)
        data["539"] = round(values[35] * 0.1, 2)

        data["92"] = bool(values[36])
        data["30"] = bool(values[37])
        #data["29"] = values[38]

        data["8"] = int(values[39])
        data["3"] = int(values[40])

        #TEST VALUE
        #data["219"] = int(values[41])

        if values[42] in ON_OFF_STATUS:
            data["143"] = ON_OFF_STATUS[values[42]]

        if values[43] in ON_OFF_STATUS:
            data["323"] = ON_OFF_STATUS[values[43]]

        if values[44] in ON_OFF_STATUS:
            data["144"] = ON_OFF_STATUS[values[44]]

        if values[45] in ON_OFF_STATUS:
            data["324"] = ON_OFF_STATUS[values[45]]   

        if values[46] in ON_OFF_STATUS:
            data["66"] = ON_OFF_STATUS[values[46]]

        if values[47] in ON_OFF_STATUS:
            data["71"] = ON_OFF_STATUS[values[47]]

        if values[48] in ON_OFF_STATUS:
            data["135"] = ON_OFF_STATUS[values[48]]

        if values[49] in ON_OFF_STATUS:
            data["72"] = ON_OFF_STATUS[values[49]]

        if values[50] in ON_OFF_STATUS:
            data["73"] = ON_OFF_STATUS[values[50]]

        if values[51] in ON_OFF_STATUS:
            data["18"] = ON_OFF_STATUS[values[51]]

        if values[52] in ON_OFF_STATUS:
            data["9"] = ON_OFF_STATUS[values[52]]

        data["60"] = int(values[53])

        if values[54] in ON_OFF_STATUS:
            data["218"] = ON_OFF_STATUS[values[54]]

        return data


    def translate_mode_code_to_messages(self, mode: int, current_mode: list) -> list:
        messages = []
        if not mode:
            return messages

        for code, mesg in current_mode:
            if mode & code:
                messages.append(mesg)    
        return messages


    def write_registers(self, address, payload) -> None:
        """Write register."""
        with self._lock:
            self._client.write_registers(address, payload, slave=1)
        