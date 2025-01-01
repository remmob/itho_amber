"""Itho Daalderop Amber 65/95/120 Modbus Hub."""

import logging
import threading
from datetime import timedelta
from voluptuous.validators import Number

# from pymodbus.register_read_message import ReadHoldingRegistersResponse
from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.exceptions import ConnectionException
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import CALLBACK_TYPE, callback, HomeAssistant

from .const import (
    DOMAIN,
    CURRENT_MODE,
    LOGIN_STATUS,
    ON_OFF_STATUS,
    PUMP_TYPE,
    CURRENT_OPERATION_MODE,
    EXTERNAL_CONTROL,
    HWTBH_PRIORITY_MODE,
    MODE_SIGNAL_TYPE,
    MODE_SIGNAL_OUTPUT,
    DISPLAY_TIME,
)

_LOGGER = logging.getLogger(__name__)

class AmberModbusHub(DataUpdateCoordinator[dict]):
    """Thread safe wrapper class for pymodbus."""

    def __init__(self, hass: HomeAssistant, name: str, host: str, port: Number, scan_interval: Number):
        """Initialize the Itho Daalderop Amber 65/95/120 Modbus hub."""
        super().__init__(hass, _LOGGER, name=name, update_interval=timedelta(seconds=scan_interval))

        self._client = ModbusTcpClient(host=host, port=port, timeout=60)
        self._lock = threading.Lock()
        self.setting_data_1: dict = {}
        self.setting_data_2: dict = {}
        self.setting_data_3: dict = {}
        self.setting_data_4: dict = {}
        self.setting_data_5: dict = {}
        self.setting_data_6: dict = {}
        self.realtime_data: dict = {}
        
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

    def _read_holding_registers(self, unit, address, count) -> None: # ReadHoldingRegistersResponse:
        """Read holding registers."""
        with self._lock:
            return self._client.read_holding_registers(address=address, count=count, slave=unit)  
    
    async def _async_update_data(self) -> dict:

        setting_data_1 = {}
        setting_data_2 = {}
        setting_data_3 = {}
        setting_data_4 = {}
        setting_data_5 = {}
        setting_data_6 = {}
        realtime_data = {}
        
 
        try:
            """Read settings data 1"""
            setting_data_1 = await self.hass.async_add_executor_job(
                   self.read_modbus_setting_data_1)

            """Read settings data 2"""
            setting_data_2 = await self.hass.async_add_executor_job(
                   self.read_modbus_setting_data_2)

            """Read settings data 3"""
            setting_data_3 = await self.hass.async_add_executor_job(
                   self.read_modbus_setting_data_3)

            """Read settings data 4"""
            setting_data_4 = await self.hass.async_add_executor_job(
                   self.read_modbus_setting_data_4)

            """Read settings data 5"""
            setting_data_5 = await self.hass.async_add_executor_job(
                   self.read_modbus_setting_data_5)

            """Read settings data 6"""
            setting_data_6 = await self.hass.async_add_executor_job(
                   self.read_modbus_setting_data_6)                   

            """Read realtime data"""
            realtime_data = await self.hass.async_add_executor_job(
                self.read_modbus_realtime_data)

        except ConnectionException:
            _LOGGER.error("Reading realtime data failed! the Itho Daalderop Amber 65/95/120 is unreachable.")

        return {**setting_data_1, **setting_data_2, **setting_data_3, **setting_data_4, **setting_data_5, **setting_data_6, **realtime_data}

    def read_modbus_setting_data_1(self) -> dict: #0 t/m 119
        """Read settings data 1"""
        setting_data_1 = self._read_holding_registers(unit=1, address=0, count=120)
        
        if setting_data_1.isError():
            return {}

        data = {}
        decoder = BinaryPayloadDecoder.fromRegisters(setting_data_1.registers, byteorder=Endian.BIG)   
        
        S0 = decoder.decode_16bit_int(); data["0"] = S0; S1 = decoder.decode_16bit_int(); data["1"] = S1; S2 = decoder.decode_16bit_int(); data["2"] = S2
        S3 = decoder.decode_16bit_int(); data["3"] = S3; S4 = decoder.decode_16bit_int(); data["4"] = S4; S5 = decoder.decode_16bit_int(); data["5"] = S5
        S6 = decoder.decode_16bit_int(); data["6"] = S6; S7 = decoder.decode_16bit_int(); data["7"] = S7; S8 = decoder.decode_16bit_int(); data["8"] = S8
        
        S9 = decoder.decode_16bit_int(); 
        if S9 in ON_OFF_STATUS:
            data ["9"] = ON_OFF_STATUS[S9] 
    
        S10 = decoder.decode_16bit_int(); data["10"] = S10; S11 = decoder.decode_16bit_int(); data["11"] = S11; S12 = decoder.decode_16bit_int(); data["12"] = S12
        S13 = decoder.decode_16bit_int(); data["13"] = S13; S14 = decoder.decode_16bit_int(); data["14"] = S14; S15 = decoder.decode_16bit_int(); data["15"] = S15
        S16 = decoder.decode_16bit_int(); data["16"] = S16; S17 = decoder.decode_16bit_int(); data["17"] = S17
        
        S18 = decoder.decode_16bit_int(); 
        if S18 in ON_OFF_STATUS:
            data ["18"] = ON_OFF_STATUS[S18]  
        
        S19 = decoder.decode_16bit_int()
        data["19"] = S19 
        S20 = decoder.decode_16bit_int()
        data["20"] = S20
        S21 = decoder.decode_16bit_int()
        data["21"] = S21
        S22 = decoder.decode_16bit_int()
        data["22"] = S22
        S23 = decoder.decode_16bit_int()
        data["23"] = S23
        S24 = decoder.decode_16bit_int()
        data["24"] = S24
        S25 = decoder.decode_16bit_int()
        data["25"] = S25

        S26 = decoder.decode_16bit_int(); data["26"] = S26; S27 = decoder.decode_16bit_int(); data["27"] = S27; S28 = decoder.decode_16bit_int(); data["28"] = S28
        S29 = decoder.decode_16bit_int(); data["29"] = S29; S30 = decoder.decode_16bit_int(); data["30"] = bool(S30)
        S31 = decoder.decode_16bit_int(); data["31"] = S31; S32 = decoder.decode_16bit_int(); data["32"] = S32; S33 = decoder.decode_16bit_int(); data["33"] = S33
        S34 = decoder.decode_16bit_int(); data["34"] = S34; S35 = decoder.decode_16bit_int(); data["35"] = S35; S36 = decoder.decode_16bit_int(); data["36"] = S36
        S37 = decoder.decode_16bit_int(); data["37"] = S37; S38 = decoder.decode_16bit_int(); data["38"] = S38; S39 = decoder.decode_16bit_int(); data["39"] = S39
        S40 = decoder.decode_16bit_int(); data["40"] = S40; S41 = decoder.decode_16bit_int(); data["41"] = S41; S42 = decoder.decode_16bit_int(); data["42"] = S42
        S43 = decoder.decode_16bit_int(); data["43"] = S43; S44 = decoder.decode_16bit_int(); data["44"] = S44; S45 = decoder.decode_16bit_int(); data["45"] = S45
        S46 = decoder.decode_16bit_int(); data["46"] = S46; S47 = decoder.decode_16bit_int(); data["47"] = S47; S48 = decoder.decode_16bit_int(); data["48"] = S48
        S49 = decoder.decode_16bit_int(); data["49"] = S49; S50 = decoder.decode_16bit_int(); data["50"] = S50; S51 = decoder.decode_16bit_int(); data["51"] = S51
        S52 = decoder.decode_16bit_int(); data["52"] = S52; S53 = decoder.decode_16bit_int(); data["53"] = S53; S54 = decoder.decode_16bit_int(); data["54"] = S54
        S55 = decoder.decode_16bit_int(); data["55"] = S55; S56 = decoder.decode_16bit_int(); data["56"] = S56; S57 = decoder.decode_16bit_int(); data["57"] = S57
        S58 = decoder.decode_16bit_int(); data["58"] = S58; S59 = decoder.decode_16bit_int(); data["59"] = S59; S60 = decoder.decode_16bit_int(); data["60"] = bool(S60)
        S61 = decoder.decode_16bit_int(); data["61"] = S61; S62 = decoder.decode_16bit_int(); data["62"] = S62; S63 = decoder.decode_16bit_int(); data["63"] = S63
        S64 = decoder.decode_16bit_int(); data["64"] = S64; S65 = decoder.decode_16bit_int(); data["65"] = S65

        S66 = decoder.decode_16bit_int(); 
        if S66 in ON_OFF_STATUS:
            data ["66"] = ON_OFF_STATUS[S66] 

        S67 = decoder.decode_16bit_int(); data["67"] = S67; S68 = decoder.decode_16bit_int(); data["68"] = S68; S69 = decoder.decode_16bit_int(); data["69"] = S69
        S70 = decoder.decode_16bit_int(); data["70"] = S70

        S71 = decoder.decode_16bit_int(); 
        if S71 in ON_OFF_STATUS:
            data ["71"] = ON_OFF_STATUS[S71] 

        S72 = decoder.decode_16bit_int(); data["72"] = S72; 
        
        S73 = decoder.decode_16bit_int(); 
        if S73 in ON_OFF_STATUS:
            data ["73"] = ON_OFF_STATUS[S73] 

        S74 = decoder.decode_16bit_int(); data["74"] = S74; S75 = decoder.decode_16bit_int(); data["75"] = S75

        S76= decoder.decode_16bit_int()
        data["76"] = S76
        S77= decoder.decode_16bit_int()
        data["77"] = S77
        S78= decoder.decode_16bit_int()
        data["78"] = S78
        S79= decoder.decode_16bit_int()
        data["79"] = S79
        S80= decoder.decode_16bit_int()
        data["80"] = S80
        S81= decoder.decode_16bit_int()
        data["81"] = S81
        S82= decoder.decode_16bit_int()
        data["82"] = S82
        S83= decoder.decode_16bit_int()
        data["83"] = S83
        S84= decoder.decode_16bit_int()
        data["84"] = S84
        S85= decoder.decode_16bit_int()
        data["85"] = S85
        S86= decoder.decode_16bit_int()
        data["86"] = S86
        S87= decoder.decode_16bit_int()
        data["87"] = S87
        S88= decoder.decode_16bit_int()
        data["88"] = S88
        S89= decoder.decode_16bit_int()
        data["89"] = S89

        S90 = decoder.decode_16bit_int(); data["90"] = bool(S90); S91 = decoder.decode_16bit_int(); data["91"] = S91; S92 = decoder.decode_16bit_int(); data["92"] = S92
        S93 = decoder.decode_16bit_int(); data["93"] = S93; S94 = decoder.decode_16bit_int(); data["94"] = S94; S95 = decoder.decode_16bit_int(); data["95"] = S95
        S96 = decoder.decode_16bit_int(); data["96"] = S96; S97 = decoder.decode_16bit_int(); data["97"] = S97; S98 = decoder.decode_16bit_int(); data["98"] = S98
        S99 = decoder.decode_16bit_int(); data["99"] = S99; S100 = decoder.decode_16bit_int(); data["100"] = S100; S101 = decoder.decode_16bit_int(); data["101"] = S101
        S102 = decoder.decode_16bit_int(); data["102"] = S102

        S103= decoder.decode_16bit_int()
        data["103"] = S103
        S104= decoder.decode_16bit_int()
        data["104"] = S104
        S105= decoder.decode_16bit_int()
        data["105"] = S105
        S106= decoder.decode_16bit_int()
        data["106"] = S106
        S107= decoder.decode_16bit_int()
        data["107"] = S107
        S108= decoder.decode_16bit_int()
        data["108"] = S108
        S109= decoder.decode_16bit_int()
        data["109"] = S109
        
        S110 = decoder.decode_16bit_int(); data["110"] = S110; S111 = decoder.decode_16bit_int(); data["111"] = S111

        S112= decoder.decode_16bit_int()
        data["112"] = S112
        S113= decoder.decode_16bit_int()
        data["113"] = S113
        S114= decoder.decode_16bit_int()
        data["114"] = S114
        S115= decoder.decode_16bit_int()
        data["115"] = S115
        S116= decoder.decode_16bit_int()
        data["116"] = S116
        S117= decoder.decode_16bit_int()
        data["117"] = S117
        S118= decoder.decode_16bit_int()
        data["118"] = S118
        
        S119 = decoder.decode_16bit_int(); 
        if S119 in MODE_SIGNAL_TYPE:
            data ["119"] = MODE_SIGNAL_TYPE[S119]

        return data

    def read_modbus_setting_data_2(self) -> dict: #120 t/m 219
        """Read settings data 2"""
        setting_data_2 = self._read_holding_registers(unit=1, address=120, count=100) #0x85
        
        if setting_data_2.isError():
            return {}

        data = {}
        decoder = BinaryPayloadDecoder.fromRegisters(setting_data_2.registers, byteorder=Endian.BIG)

        S120 = decoder.decode_16bit_int() 
        if S120 in ON_OFF_STATUS:
            data ["120"] = ON_OFF_STATUS[S120]

        S121 = decoder.decode_16bit_int() 
        if S121 in ON_OFF_STATUS:
            data ["121"] = ON_OFF_STATUS[S121]

        S122 = decoder.decode_16bit_int()
        if S122 in ON_OFF_STATUS:
            data ["122"] = ON_OFF_STATUS[S122]

        S123 = decoder.decode_16bit_int(); data["123"] = S123; S124 = decoder.decode_16bit_int(); data["124"] = S124; S125 = decoder.decode_16bit_int(); data["125"] = S125
        
        S126 = decoder.decode_16bit_int()
        if S126 in DISPLAY_TIME:
            data["126"] = DISPLAY_TIME[S126] 
        
        S127 = decoder.decode_16bit_int(); data["127"] = S127; S128 = decoder.decode_16bit_int(); data["128"] = S128; S129 = decoder.decode_16bit_int(); data["129"] = S129
        S130 = decoder.decode_16bit_int(); data["130"] = S130; S131 = decoder.decode_16bit_int(); data["131"] = S131; S132 = decoder.decode_16bit_int(); data["132"] = S132
        S133 = decoder.decode_16bit_int(); data["133"] = S133; S134 = decoder.decode_16bit_int(); data["134"] = S134; S135 = decoder.decode_16bit_int(); data["135"] = bool(S135)
        S136 = decoder.decode_16bit_int(); data["136"] = S136
       
        S137 = decoder.decode_16bit_int()
        if S137 in PUMP_TYPE:
            data ["137"] = PUMP_TYPE[S137]

        S138 = decoder.decode_16bit_int(); data["138"] = S138; S139 = decoder.decode_16bit_int(); data["139"] = S139; S140 = decoder.decode_16bit_int(); data["140"] = S140
        S141 = decoder.decode_16bit_int(); data["141"] = S141; S142 = decoder.decode_16bit_int(); data["142"] = S142

        S143 = decoder.decode_16bit_int()
        if S143 in ON_OFF_STATUS:
            data ["143"] = ON_OFF_STATUS[S143]
       
        S144 = decoder.decode_16bit_int()
        if S144 in ON_OFF_STATUS:
            data ["144"] = ON_OFF_STATUS[S144]

        S145 = decoder.decode_16bit_int()
        if S145 in ON_OFF_STATUS:
            data ["145"] = ON_OFF_STATUS[S145]

        S146 = decoder.decode_16bit_int()
        if S146 in ON_OFF_STATUS:
            data ["146"] = ON_OFF_STATUS[S146]

        S147 = decoder.decode_16bit_int()
        if S147 in ON_OFF_STATUS:
            data ["147"] = ON_OFF_STATUS[S147]

        S148 = decoder.decode_16bit_int()
        if S148 in ON_OFF_STATUS:
            data ["148"] = ON_OFF_STATUS[S148]

        S149 = decoder.decode_16bit_int()
        if S149 in ON_OFF_STATUS:
            data ["149"] = ON_OFF_STATUS[S149]

        S150 = decoder.decode_16bit_int()
        if S150 in ON_OFF_STATUS:
            data ["150"] = ON_OFF_STATUS[S150]

        S151 = decoder.decode_16bit_int(); data["151"] = S151; S152 = decoder.decode_16bit_int(); data["152"] = S152; S153 = decoder.decode_16bit_int(); data["153"] = S153
        S154 = decoder.decode_16bit_int(); data["154"] = S154; S155 = decoder.decode_16bit_int(); data["155"] = S155; S156 = decoder.decode_16bit_int(); data["156"] = S156
        S157 = decoder.decode_16bit_int(); data["157"] = S157; S158 = decoder.decode_16bit_int(); data["158"] = S158; S159 = decoder.decode_16bit_int(); data["159"] = S159
        S160 = decoder.decode_16bit_int(); data["160"] = S160; S161 = decoder.decode_16bit_int(); data["161"] = S161; S162 = decoder.decode_16bit_int(); data["162"] = S162
        S163 = decoder.decode_16bit_int(); data["163"] = S163; S164 = decoder.decode_16bit_int(); data["164"] = S164; S165 = decoder.decode_16bit_int(); data["165"] = S165
        S166 = decoder.decode_16bit_int(); data["166"] = S166; S167 = decoder.decode_16bit_int(); data["167"] = S167; S168 = decoder.decode_16bit_int(); data["168"] = S168
        S169 = decoder.decode_16bit_int(); data["169"] = S169; S170 = decoder.decode_16bit_int(); data["170"] = S170; S171 = decoder.decode_16bit_int(); data["171"] = S171
        S172 = decoder.decode_16bit_int(); data["172"] = S172; S173 = decoder.decode_16bit_int(); data["173"] = S173; S174 = decoder.decode_16bit_int(); data["174"] = S174
        S175 = decoder.decode_16bit_int(); data["175"] = S175; S176 = decoder.decode_16bit_int(); data["176"] = S176; S177 = decoder.decode_16bit_int(); data["177"] = S177
        S178 = decoder.decode_16bit_int(); data["178"] = S178; S179 = decoder.decode_16bit_int(); data["179"] = S179; S180 = decoder.decode_16bit_int(); data["180"] = S180
        S181 = decoder.decode_16bit_int(); data["181"] = S181; S182 = decoder.decode_16bit_int(); data["182"] = S182; S183 = decoder.decode_16bit_int(); data["183"] = S183
        S184 = decoder.decode_16bit_int(); data["184"] = S184; S185 = decoder.decode_16bit_int(); data["185"] = S185; S186 = decoder.decode_16bit_int(); data["186"] = S186
        S187 = decoder.decode_16bit_int(); data["187"] = S187; S188 = decoder.decode_16bit_int(); data["188"] = S188; S189 = decoder.decode_16bit_int(); data["189"] = S189
        S190 = decoder.decode_16bit_int(); data["190"] = S190; S191 = decoder.decode_16bit_int(); data["191"] = S191; S192 = decoder.decode_16bit_int(); data["192"] = S192
        S193 = decoder.decode_16bit_int(); data["193"] = S193; S194 = decoder.decode_16bit_int(); data["194"] = S194; S195 = decoder.decode_16bit_int(); data["195"] = S195
        S196 = decoder.decode_16bit_int(); data["196"] = S196; S197 = decoder.decode_16bit_int(); data["197"] = S197; S198 = decoder.decode_16bit_int(); data["198"] = S198
        S199 = decoder.decode_16bit_int(); data["199"] = S199; S200 = decoder.decode_16bit_int(); data["200"] = S200; S201 = decoder.decode_16bit_int(); data["201"] = S201

        S202 = decoder.decode_16bit_int()
        if S202 in MODE_SIGNAL_OUTPUT:
            data ["202"] = MODE_SIGNAL_OUTPUT[S202]

        S203 = decoder.decode_16bit_int()
        if S203 in MODE_SIGNAL_TYPE:
            data ["203"] = MODE_SIGNAL_TYPE[S203]

        S204 = decoder.decode_16bit_int(); data["204"] = S204; S205 = decoder.decode_16bit_int(); data["205"] = S205; S206 = decoder.decode_16bit_int(); data["206"] = S206
        S207 = decoder.decode_16bit_int(); data["207"] = S207; S208 = decoder.decode_16bit_int(); data["208"] = S208; S209 = decoder.decode_16bit_int(); data["209"] = S209
        S210 = decoder.decode_16bit_int(); data["210"] = S210; S211 = decoder.decode_16bit_int(); data["211"] = S211; S212 = decoder.decode_16bit_int(); data["212"] = S212
        S213 = decoder.decode_16bit_int(); data["213"] = S213; S214 = decoder.decode_16bit_int(); data["214"] = S214; S215 = decoder.decode_16bit_int(); data["215"] = S215
        S216 = decoder.decode_16bit_int(); data["216"] = S216; S217 = decoder.decode_16bit_int(); data["217"] = S217

        S218 = decoder.decode_16bit_int()
        if S218 in ON_OFF_STATUS:
            data ["218"] = ON_OFF_STATUS[S218]

        S219 = decoder.decode_16bit_int(); data["219"] = S219

        return data

    def read_modbus_setting_data_3(self) -> dict: #314 t/m 324
        """Read settings data 3"""
        setting_data_3 = self._read_holding_registers(unit=1, address=314, count=11)
        
        if setting_data_3.isError():
            return {}

        data = {}
        decoder = BinaryPayloadDecoder.fromRegisters(setting_data_3.registers, byteorder=Endian.BIG)

        S314 = decoder.decode_16bit_int(); data["314"] = S314; S315 = decoder.decode_16bit_int(); data["315"] = S315; S316 = decoder.decode_16bit_int(); data["316"] = S316
        S317 = decoder.decode_16bit_int(); data["317"] = S317; S318 = decoder.decode_16bit_int(); data["318"] = S318; S319 = decoder.decode_16bit_int(); data["319"] = S319
        S320 = decoder.decode_16bit_int(); data["320"] = S320; S321 = decoder.decode_16bit_int(); data["321"] = S321; S322 = decoder.decode_16bit_int(); data["322"] = S322
        
        S323 = decoder.decode_16bit_int()
        if S323 in ON_OFF_STATUS:
            data ["323"] = ON_OFF_STATUS[S323]

        S324= decoder.decode_16bit_int()
        if S324 in ON_OFF_STATUS:
            data ["324"] = ON_OFF_STATUS[S324]

        return data

    def read_modbus_setting_data_4(self) -> dict: #399 & 340
        """Read settings data 4"""
        setting_data_4 = self._read_holding_registers(unit=1, address=339, count=2)
        
        if setting_data_4.isError():
            return {}

        data = {}
        decoder = BinaryPayloadDecoder.fromRegisters(setting_data_4.registers, byteorder=Endian.BIG)

        S339 = decoder.decode_16bit_int()
        if S339 in ON_OFF_STATUS:
            data ["339"] = ON_OFF_STATUS[S339]

        S340 = decoder.decode_16bit_int(); data["340"] = S340

        return data

    def read_modbus_setting_data_5(self) -> dict: #375 & 376
        """Read settings data 5"""
        setting_data_5 = self._read_holding_registers(unit=1, address=375, count=2)
        
        if setting_data_5.isError():
            return {}

        data = {}
        decoder = BinaryPayloadDecoder.fromRegisters(setting_data_5.registers, byteorder=Endian.BIG)

        S375 = decoder.decode_16bit_int(); data["375"] = S375; S376 = decoder.decode_16bit_int(); data["376"] = S376

        return data

    def read_modbus_setting_data_6(self) -> dict: #407 t/m 459
        """Read settings data 6"""
        setting_data_6 = self._read_holding_registers(unit=1, address=407, count=53)
        
        if setting_data_6.isError():
            return {}

        data = {}
        decoder = BinaryPayloadDecoder.fromRegisters(setting_data_6.registers, byteorder=Endian.BIG)

        S407 = decoder.decode_16bit_int(); data["407"] = S407
        S408 = decoder.decode_16bit_int(); data["408"] = S408
        S409 = decoder.decode_16bit_int(); data["409"] = S409
        S410 = decoder.decode_16bit_int(); data["410"] = S410
        S411 = decoder.decode_16bit_int(); data["411"] = S411
        S412 = decoder.decode_16bit_int(); data["412"] = S412
        S413 = decoder.decode_16bit_int(); data["413"] = S413
        S414 = decoder.decode_16bit_int(); data["414"] = S414
        S415 = decoder.decode_16bit_int(); data["415"] = S415
        S416 = decoder.decode_16bit_int(); data["416"] = S416
        S417 = decoder.decode_16bit_int(); data["417"] = S417
        S418 = decoder.decode_16bit_int(); data["418"] = S418
        S419 = decoder.decode_16bit_int(); data["419"] = S419
        S420 = decoder.decode_16bit_int(); data["420"] = S420
        S421 = decoder.decode_16bit_int(); data["421"] = S421
        S422 = decoder.decode_16bit_int(); data["422"] = S422
        S423 = decoder.decode_16bit_int(); data["423"] = S423
        S424 = decoder.decode_16bit_int(); data["424"] = S424
        S425 = decoder.decode_16bit_int(); data["425"] = S425
        S426 = decoder.decode_16bit_int(); data["426"] = S426
        S427 = decoder.decode_16bit_int(); data["427"] = S427
        S428 = decoder.decode_16bit_int(); data["428"] = S428
        S429 = decoder.decode_16bit_int(); data["429"] = S429
        S430 = decoder.decode_16bit_int(); data["430"] = S430
        S431 = decoder.decode_16bit_int(); data["431"] = S431
        S432 = decoder.decode_16bit_int(); data["432"] = S432
        S433 = decoder.decode_16bit_int(); data["433"] = S433
        S434 = decoder.decode_16bit_int(); data["434"] = S434
        S435 = decoder.decode_16bit_int(); data["435"] = S435
        S436 = decoder.decode_16bit_int(); data["436"] = S436
        S437 = decoder.decode_16bit_int(); data["437"] = S437
        S438 = decoder.decode_16bit_int(); data["438"] = S438
        S439 = decoder.decode_16bit_int(); data["439"] = S439
        S440 = decoder.decode_16bit_int(); data["440"] = S440
        S441 = decoder.decode_16bit_int(); data["441"] = S441
        S442 = decoder.decode_16bit_int(); data["442"] = S442
        S443 = decoder.decode_16bit_int(); data["443"] = S443
        S444 = decoder.decode_16bit_int(); data["444"] = S444
        S445 = decoder.decode_16bit_int(); data["445"] = S445
        S446 = decoder.decode_16bit_int(); data["446"] = S446
        S447 = decoder.decode_16bit_int(); data["447"] = S447
        S448 = decoder.decode_16bit_int(); data["448"] = S448
        S449 = decoder.decode_16bit_int(); data["449"] = S449
        S450 = decoder.decode_16bit_int(); data["450"] = S450
        S451 = decoder.decode_16bit_int(); data["450"] = S451
        S452 = decoder.decode_16bit_int(); data["452"] = S452
        S453 = decoder.decode_16bit_int(); data["453"] = S453
        S454 = decoder.decode_16bit_int(); data["454"] = S454
        S455 = decoder.decode_16bit_int(); data["455"] = S455
        S456 = decoder.decode_16bit_int(); data["456"] = S456
        S457 = decoder.decode_16bit_int(); data["457"] = S457
        S458 = decoder.decode_16bit_int(); data["458"] = S458
        S459 = decoder.decode_16bit_int(); data["459"] = S459

        return data

    def read_modbus_realtime_data(self) -> dict: # 499 t/m 539mB
        """Read the reatime sensor values"""
        realtime_data = self._read_holding_registers(unit=1, address=499, count=41)

        if realtime_data.isError():
            return {}

        data = {}
        decoder = BinaryPayloadDecoder.fromRegisters(realtime_data.registers, byteorder=Endian.BIG)

        mode = decoder.decode_16bit_int()
        _mode = []
        _mode.extend(self.translate_mode_code_to_messages(mode, CURRENT_MODE.items()))
        data["499"] = ", ".join(_mode).strip()[0:254]

        S500 = decoder.decode_16bit_int()
        if S500 in LOGIN_STATUS:
            data["500"] = LOGIN_STATUS[S500]

        S501 = decoder.decode_16bit_int(); data["501"] = round(S501 * 0.01,2)
        S502 = decoder.decode_16bit_int(); data["502"] = S502
        S503 = decoder.decode_16bit_int(); data["503"] = round(S503 * 0.01, 2)
        S504 = decoder.decode_16bit_int(); data["504"] = round(S504 * 0.01, 2)
        S505 = decoder.decode_16bit_int(); data["505"] = round(S505 * 0.1, 2)
        S506 = decoder.decode_16bit_int(); data["506"] = round(S506 * 0.1, 2)
        S507 = decoder.decode_16bit_int(); data["507"] = round(S507 * 0.1, 2)
        S508 = decoder.decode_16bit_int(); data["508"] = round(S508 * 0.1, 2)
        S509 = decoder.decode_16bit_int(); data["509"] = round(S509 * 0.1, 2)
        S510 = decoder.decode_16bit_int(); data["510"] = round(S510 * 0.1, 2)
        S511 = decoder.decode_16bit_int(); data["511"] = round(S511 * 0.1, 2)
        S512 = decoder.decode_16bit_int(); data["512"] = S512
        S513 = decoder.decode_16bit_int(); data["513"] = S513

        S514 = decoder.decode_16bit_int()
        if S514 in CURRENT_OPERATION_MODE:
            data["514"] = CURRENT_OPERATION_MODE[S514]

        S515 = decoder.decode_16bit_int(); data["515"] = S515
        S516 = decoder.decode_16bit_int(); data["516"] = S516
        S517 = decoder.decode_16bit_int(); data["517"] = round(S517 * 0.1, 2)
        S518 = decoder.decode_16bit_int(); data["518"] = round(S518 * 0.1, 2)
        S519 = decoder.decode_16bit_int(); data["519"] = round(S519 * 0.1, 2)
        S520 = decoder.decode_16bit_int(); data["520"] = round(S520 * 0.1, 2)
        S521 = decoder.decode_16bit_int(); data["521"] = round(S521 * 0.1, 2)
        S522 = decoder.decode_16bit_int(); data["522"] = round(S522 * 0.1, 2)
        S523 = decoder.decode_16bit_int(); data["523"] = round(S523 * 0.1, 2)
        S524 = decoder.decode_16bit_int(); data["524"] = round(S524 * 0.1, 2)
        S525 = decoder.decode_16bit_int(); data["525"] = round(S525 * 0.1, 2)
        S526 = decoder.decode_16bit_int(); data["526"] = S526
        S527 = decoder.decode_16bit_int(); data["527"] = S527
        S528 = decoder.decode_16bit_int(); data["528"] = round(S528 * 0.1, 2)
        S529 = decoder.decode_16bit_int(); data["529"] = S529

        S530 = decoder.decode_16bit_int()
        if S530 in ON_OFF_STATUS:
            data["530"] = ON_OFF_STATUS[S530]

        S531 = decoder.decode_16bit_int(); data["531"] = round(S531 * 0.1, 2)

        S532 = decoder.decode_16bit_int()
        if S532 in ON_OFF_STATUS:
            data["532"] = ON_OFF_STATUS[S532]

        S533 = decoder.decode_16bit_int()
        if S533 in ON_OFF_STATUS:
            data["533"] = ON_OFF_STATUS[S533]

        S534 = decoder.decode_16bit_int()
        if S534 in ON_OFF_STATUS:
            data["534"] = ON_OFF_STATUS[S534]
        
        S535 = decoder.decode_16bit_int()
        if S535 in ON_OFF_STATUS:
            data["535"] = ON_OFF_STATUS[S535]

        S536 = decoder.decode_16bit_int()
        if S536 in ON_OFF_STATUS:
            data["536"] = ON_OFF_STATUS[S536]

        S537 = decoder.decode_16bit_int(); data["537"] = round(S537 * 0.1)
        S538 = decoder.decode_16bit_int(); data["538"] = round(S538 * 0.1, 2)
        S539 = decoder.decode_16bit_int(); data["539"] = round(S539 * 0.1, 2)

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
     