"""Itho Daalderop Amber 65/95/120 Modbus Hub."""

import logging
import threading
from datetime import timedelta
from voluptuous.validators import Number

from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.exceptions import ConnectionException

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

    def _read_holding_registers(self, unit, address, count) -> None:
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
        newdecoder = ModbusTcpClient.convert_from_registers(setting_data_1.registers, data_type=ModbusTcpClient.DATATYPE.INT16) 

        S0 = newdecoder[0]; data["0"] = S0; S1 = newdecoder[1]; data["1"] = S1; S2 = newdecoder[2]; data["2"] = S2
        S3 = newdecoder[3]; data["3"] = S3; S4 = newdecoder[4]; data["4"] = S4; S5 = newdecoder[5]; data["5"] = S5
        S6 = newdecoder[6]; data["6"] = S6; S7 = newdecoder[7]; data["7"] = S7; S8 = newdecoder[8]; data["8"] = S8
        
        S9 = newdecoder[9]; 
        if S9 in ON_OFF_STATUS:
            data ["9"] = ON_OFF_STATUS[S9] 
    
        S10 = newdecoder[10]; data["10"] = S10; S11 = newdecoder[11]; data["11"] = S11; S12 = newdecoder[12]; data["12"] = S12
        S13 = newdecoder[13]; data["13"] = S13; S14 = newdecoder[14]; data["14"] = S14; S15 = newdecoder[15]; data["15"] = S15
        S16 = newdecoder[16]; data["16"] = S16; S17 = newdecoder[17]; data["17"] = S17
        
        S18 = newdecoder[18]; 
        if S18 in ON_OFF_STATUS:
            data ["18"] = ON_OFF_STATUS[S18]  
        
        S19 = newdecoder[19]
        data["19"] = S19 
        S20 = newdecoder[20]
        data["20"] = S20
        S21 = newdecoder[21]
        data["21"] = S21
        S22 = newdecoder[22]
        data["22"] = S22
        S23 = newdecoder[23]
        data["23"] = S23
        S24 = newdecoder[24]
        data["24"] = S24
        S25 = newdecoder[25]
        data["25"] = S25

        S26 = newdecoder[26]; data["26"] = S26; S27 = newdecoder[27]; data["27"] = S27; S28 = newdecoder[28]; data["28"] = S28
        S29 = newdecoder[29]; data["29"] = S29; S30 = newdecoder[30]; data["30"] = bool(S30)
        S31 = newdecoder[31]; data["31"] = S31; S32 = newdecoder[32]; data["32"] = S32; S33 = newdecoder[33]; data["33"] = S33
        S34 = newdecoder[34]; data["34"] = S34; S35 = newdecoder[35]; data["35"] = S35; S36 = newdecoder[36]; data["36"] = S36
        S37 = newdecoder[37]; data["37"] = S37; S38 = newdecoder[38]; data["38"] = S38; S39 = newdecoder[39]; data["39"] = S39
        S40 = newdecoder[40]; data["40"] = S40; S41 = newdecoder[41]; data["41"] = S41; S42 = newdecoder[42]; data["42"] = S42
        S43 = newdecoder[43]; data["43"] = S43; S44 = newdecoder[44]; data["44"] = S44; S45 = newdecoder[45]; data["45"] = S45
        S46 = newdecoder[46]; data["46"] = S46; S47 = newdecoder[47]; data["47"] = S47; S48 = newdecoder[48]; data["48"] = S48
        S49 = newdecoder[49]; data["49"] = S49; S50 = newdecoder[50]; data["50"] = S50; S51 = newdecoder[51]; data["51"] = S51
        S52 = newdecoder[52]; data["52"] = S52; S53 = newdecoder[53]; data["53"] = S53; S54 = newdecoder[54]; data["54"] = S54
        S55 = newdecoder[55]; data["55"] = S55; S56 = newdecoder[56]; data["56"] = S56; S57 = newdecoder[57]; data["57"] = S57
        S58 = newdecoder[58]; data["58"] = S58; S59 = newdecoder[59]; data["59"] = S59; S60 = newdecoder[60]; data["60"] = bool(S60)
        S61 = newdecoder[61]; data["61"] = S61; S62 = newdecoder[62]; data["62"] = S62; S63 = newdecoder[63]; data["63"] = S63
        S64 = newdecoder[64]; data["64"] = S64; S65 = newdecoder[65]; data["65"] = S65

        S66 = newdecoder[66]; 
        if S66 in ON_OFF_STATUS:
            data ["66"] = ON_OFF_STATUS[S66] 

        S67 = newdecoder[67]; data["67"] = S67; S68 = newdecoder[68]; data["68"] = S68; S69 = newdecoder[69]; data["69"] = S69
        S70 = newdecoder[70]; data["70"] = S70

        S71 = newdecoder[71]; 
        if S71 in ON_OFF_STATUS:
            data ["71"] = ON_OFF_STATUS[S71] 

        S72 = newdecoder[72]; data["72"] = S72; 
        
        S73 = newdecoder[73]; 
        if S73 in ON_OFF_STATUS:
            data ["73"] = ON_OFF_STATUS[S73] 

        S74 = newdecoder[74]; data["74"] = S74; S75 = newdecoder[75]; data["75"] = S75

        S76= newdecoder[76]
        data["76"] = S76
        S77= newdecoder[77]
        data["77"] = S77
        S78= newdecoder[78]
        data["78"] = S78
        S79= newdecoder[79]
        data["79"] = S79
        S80= newdecoder[80]
        data["80"] = S80
        S81= newdecoder[81]
        data["81"] = S81
        S82= newdecoder[82]
        data["82"] = S82
        S83= newdecoder[83]
        data["83"] = S83
        S84= newdecoder[84]
        data["84"] = S84
        S85= newdecoder[85]
        data["85"] = S85
        S86= newdecoder[86]
        data["86"] = S86
        S87= newdecoder[87]
        data["87"] = S87
        S88= newdecoder[88]
        data["88"] = S88
        S89= newdecoder[89]
        data["89"] = S89

        S90 = newdecoder[90]; data["90"] = bool(S90); S91 = newdecoder[91]; data["91"] = S91; S92 = newdecoder[92]; data["92"] = S92
        S93 = newdecoder[93]; data["93"] = S93; S94 = newdecoder[94]; data["94"] = S94; S95 = newdecoder[95]; data["95"] = S95
        S96 = newdecoder[96]; data["96"] = S96; S97 = newdecoder[97]; data["97"] = S97; S98 = newdecoder[98]; data["98"] = S98
        S99 = newdecoder[99]; data["99"] = S99; S100 = newdecoder[100]; data["100"] = S100; S101 = newdecoder[101]; data["101"] = S101
        S102 = newdecoder[102]; data["102"] = S102

        S103= newdecoder[103]
        data["103"] = S103
        S104= newdecoder[104]
        data["104"] = S104
        S105= newdecoder[105]
        data["105"] = S105
        S106= newdecoder[106]
        data["106"] = S106
        S107= newdecoder[107]
        data["107"] = S107
        S108= newdecoder[108]
        data["108"] = S108
        S109= newdecoder[109]
        data["109"] = S109
        
        S110 = newdecoder[110]; data["110"] = S110; S111 = newdecoder[111]; data["111"] = S111

        S112= newdecoder[112]
        data["112"] = S112
        S113= newdecoder[113]
        data["113"] = S113
        S114= newdecoder[114]
        data["114"] = S114
        S115= newdecoder[115]
        data["115"] = S115
        S116= newdecoder[116]
        data["116"] = S116
        S117= newdecoder[117]
        data["117"] = S117
        S118= newdecoder[118]
        data["118"] = S118
        
        S119 = newdecoder[119]; 
        if S119 in MODE_SIGNAL_TYPE:
            data ["119"] = MODE_SIGNAL_TYPE[S119]

        return data

    def read_modbus_setting_data_2(self) -> dict: #120 t/m 219
        """Read settings data 2"""
        setting_data_2 = self._read_holding_registers(unit=1, address=120, count=100) #0x85
        
        if setting_data_2.isError():
            return {}

        data = {}
        newdecoder = ModbusTcpClient.convert_from_registers(setting_data_2.registers, data_type=ModbusTcpClient.DATATYPE.INT16)

        S120 = newdecoder[0] 
        if S120 in ON_OFF_STATUS:
            data ["120"] = ON_OFF_STATUS[S120]

        S121 = newdecoder[1] 
        if S121 in ON_OFF_STATUS:
            data ["121"] = ON_OFF_STATUS[S121]

        S122 = newdecoder[2]
        if S122 in ON_OFF_STATUS:
            data ["122"] = ON_OFF_STATUS[S122]

        S123 = newdecoder[3]; data["123"] = S123; S124 = newdecoder[4]; data["124"] = S124; S125 = newdecoder[5]; data["125"] = S125
        
        S126 = newdecoder[6]
        if S126 in DISPLAY_TIME:
            data["126"] = DISPLAY_TIME[S126] 
        
        S127 = newdecoder[7]; data["127"] = S127; S128 = newdecoder[8]; data["128"] = S128; S129 = newdecoder[9]; data["129"] = S129
        S130 = newdecoder[10]; data["130"] = S130; S131 = newdecoder[11]; data["131"] = S131; S132 = newdecoder[12]; data["132"] = S132
        S133 = newdecoder[13]; data["133"] = S133; S134 = newdecoder[14]; data["134"] = S134; S135 = newdecoder[15]; data["135"] = bool(S135)
        S136 = newdecoder[16]; data["136"] = S136
       
        S137 = newdecoder[17]
        if S137 in PUMP_TYPE:
            data ["137"] = PUMP_TYPE[S137]

        S138 = newdecoder[18]; data["138"] = S138; S139 = newdecoder[19]; data["139"] = S139; S140 = newdecoder[20]; data["140"] = S140
        S141 = newdecoder[21]; data["141"] = S141; S142 = newdecoder[22]; data["142"] = S142

        S143 = newdecoder[23]
        if S143 in ON_OFF_STATUS:
            data ["143"] = ON_OFF_STATUS[S143]
       
        S144 = newdecoder[24]
        if S144 in ON_OFF_STATUS:
            data ["144"] = ON_OFF_STATUS[S144]

        S145 = newdecoder[25]
        if S145 in ON_OFF_STATUS:
            data ["145"] = ON_OFF_STATUS[S145]

        S146 = newdecoder[26]
        if S146 in ON_OFF_STATUS:
            data ["146"] = ON_OFF_STATUS[S146]

        S147 = newdecoder[27]
        if S147 in ON_OFF_STATUS:
            data ["147"] = ON_OFF_STATUS[S147]

        S148 = newdecoder[28]
        if S148 in ON_OFF_STATUS:
            data ["148"] = ON_OFF_STATUS[S148]

        S149 = newdecoder[29]
        if S149 in ON_OFF_STATUS:
            data ["149"] = ON_OFF_STATUS[S149]

        S150 = newdecoder[30]
        if S150 in ON_OFF_STATUS:
            data ["150"] = ON_OFF_STATUS[S150]

        S151 = newdecoder[31]; data["151"] = S151; S152 = newdecoder[32]; data["152"] = S152; S153 = newdecoder[33]; data["153"] = S153
        S154 = newdecoder[34]; data["154"] = S154; S155 = newdecoder[35]; data["155"] = S155; S156 = newdecoder[36]; data["156"] = S156
        S157 = newdecoder[37]; data["157"] = S157; S158 = newdecoder[38]; data["158"] = S158; S159 = newdecoder[39]; data["159"] = S159
        S160 = newdecoder[40]; data["160"] = S160; S161 = newdecoder[41]; data["161"] = S161; S162 = newdecoder[42]; data["162"] = S162
        S163 = newdecoder[43]; data["163"] = S163; S164 = newdecoder[44]; data["164"] = S164; S165 = newdecoder[45]; data["165"] = S165
        S166 = newdecoder[46]; data["166"] = S166; S167 = newdecoder[47]; data["167"] = S167; S168 = newdecoder[48]; data["168"] = S168
        S169 = newdecoder[49]; data["169"] = S169; S170 = newdecoder[50]; data["170"] = S170; S171 = newdecoder[51]; data["171"] = S171
        S172 = newdecoder[52]; data["172"] = S172; S173 = newdecoder[53]; data["173"] = S173; S174 = newdecoder[54]; data["174"] = S174
        S175 = newdecoder[55]; data["175"] = S175; S176 = newdecoder[56]; data["176"] = S176; S177 = newdecoder[57]; data["177"] = S177
        S178 = newdecoder[58]; data["178"] = S178; S179 = newdecoder[59]; data["179"] = S179; S180 = newdecoder[60]; data["180"] = S180
        S181 = newdecoder[61]; data["181"] = S181; S182 = newdecoder[62]; data["182"] = S182; S183 = newdecoder[63]; data["183"] = S183
        S184 = newdecoder[64]; data["184"] = S184; S185 = newdecoder[65]; data["185"] = S185; S186 = newdecoder[66]; data["186"] = S186
        S187 = newdecoder[67]; data["187"] = S187; S188 = newdecoder[68]; data["188"] = S188; S189 = newdecoder[69]; data["189"] = S189
        S190 = newdecoder[70]; data["190"] = S190; S191 = newdecoder[71]; data["191"] = S191; S192 = newdecoder[72]; data["192"] = S192
        S193 = newdecoder[73]; data["193"] = S193; S194 = newdecoder[74]; data["194"] = S194; S195 = newdecoder[75]; data["195"] = S195
        S196 = newdecoder[76]; data["196"] = S196; S197 = newdecoder[77]; data["197"] = S197; S198 = newdecoder[78]; data["198"] = S198
        S199 = newdecoder[79]; data["199"] = S199; S200 = newdecoder[80]; data["200"] = S200; S201 = newdecoder[81]; data["201"] = S201

        S202 = newdecoder[82]
        if S202 in MODE_SIGNAL_OUTPUT:
            data ["202"] = MODE_SIGNAL_OUTPUT[S202]

        S203 = newdecoder[83]
        if S203 in MODE_SIGNAL_TYPE:
            data ["203"] = MODE_SIGNAL_TYPE[S203]

        S204 = newdecoder[84]; data["204"] = S204; S205 = newdecoder[85]; data["205"] = S205; S206 = newdecoder[86]; data["206"] = S206
        S207 = newdecoder[87]; data["207"] = S207; S208 = newdecoder[88]; data["208"] = S208; S209 = newdecoder[89]; data["209"] = S209
        S210 = newdecoder[90]; data["210"] = S210; S211 = newdecoder[91]; data["211"] = S211; S212 = newdecoder[92]; data["212"] = S212
        S213 = newdecoder[93]; data["213"] = S213; S214 = newdecoder[94]; data["214"] = S214; S215 = newdecoder[95]; data["215"] = S215
        S216 = newdecoder[96]; data["216"] = S216; S217 = newdecoder[97]; data["217"] = S217

        S218 = newdecoder[98]
        if S218 in ON_OFF_STATUS:
            data ["218"] = ON_OFF_STATUS[S218]

        S219 = newdecoder[99]; data["219"] = S219

        return data

    def read_modbus_setting_data_3(self) -> dict: #314 t/m 324
        """Read settings data 3"""
        setting_data_3 = self._read_holding_registers(unit=1, address=314, count=11)
        
        if setting_data_3.isError():
            return {}

        data = {}
        newdecoder = ModbusTcpClient.convert_from_registers(setting_data_3.registers, data_type=ModbusTcpClient.DATATYPE.INT16)

        S314 = newdecoder[0]; data["314"] = S314; S315 = newdecoder[1]; data["315"] = S315; S316 = newdecoder[2]; data["316"] = S316
        S317 = newdecoder[3]; data["317"] = S317; S318 = newdecoder[4]; data["318"] = S318; S319 = newdecoder[5]; data["319"] = S319
        S320 = newdecoder[6]; data["320"] = S320; S321 = newdecoder[7]; data["321"] = S321; S322 = newdecoder[8]; data["322"] = S322
        
        S323 = newdecoder[9]
        if S323 in ON_OFF_STATUS:
            data ["323"] = ON_OFF_STATUS[S323]

        S324= newdecoder[10]
        if S324 in ON_OFF_STATUS:
            data ["324"] = ON_OFF_STATUS[S324]

        return data

    def read_modbus_setting_data_4(self) -> dict: #399 & 340
        """Read settings data 4"""
        setting_data_4 = self._read_holding_registers(unit=1, address=339, count=2)
        
        if setting_data_4.isError():
            return {}

        data = {}
        newdecoder = ModbusTcpClient.convert_from_registers(setting_data_4.registers, data_type=ModbusTcpClient.DATATYPE.INT16)

        S339 = newdecoder[0]
        if S339 in ON_OFF_STATUS:
            data ["339"] = ON_OFF_STATUS[S339]

        S340 = newdecoder[1]; data["340"] = S340

        return data

    def read_modbus_setting_data_5(self) -> dict: #375 & 376
        """Read settings data 5"""
        setting_data_5 = self._read_holding_registers(unit=1, address=375, count=2)
        
        if setting_data_5.isError():
            return {}

        data = {}
        newdecoder = ModbusTcpClient.convert_from_registers(setting_data_5.registers, data_type=ModbusTcpClient.DATATYPE.INT16)

        S375 = newdecoder[0]; data["375"] = S375; S376 = newdecoder[1]; data["376"] = S376

        return data

    def read_modbus_setting_data_6(self) -> dict: #407 t/m 459
        """Read settings data 6"""
        setting_data_6 = self._read_holding_registers(unit=1, address=407, count=53)
        
        if setting_data_6.isError():
            return {}

        data = {}
        newdecoder = ModbusTcpClient.convert_from_registers(setting_data_6.registers, data_type=ModbusTcpClient.DATATYPE.INT16)

        S407 = newdecoder[0]; data["407"] = S407
        S408 = newdecoder[1]; data["408"] = S408
        S409 = newdecoder[2]; data["409"] = S409
        S410 = newdecoder[3]; data["410"] = S410
        S411 = newdecoder[4]; data["411"] = S411
        S412 = newdecoder[5]; data["412"] = S412
        S413 = newdecoder[6]; data["413"] = S413
        S414 = newdecoder[7]; data["414"] = S414
        S415 = newdecoder[8]; data["415"] = S415
        S416 = newdecoder[9]; data["416"] = S416
        S417 = newdecoder[10]; data["417"] = S417
        S418 = newdecoder[11]; data["418"] = S418
        S419 = newdecoder[12]; data["419"] = S419
        S420 = newdecoder[13]; data["420"] = S420
        S421 = newdecoder[14]; data["421"] = S421
        S422 = newdecoder[15]; data["422"] = S422
        S423 = newdecoder[16]; data["423"] = S423
        S424 = newdecoder[17]; data["424"] = S424
        S425 = newdecoder[18]; data["425"] = S425
        S426 = newdecoder[19]; data["426"] = S426
        S427 = newdecoder[20]; data["427"] = S427
        S428 = newdecoder[21]; data["428"] = S428
        S429 = newdecoder[22]; data["429"] = S429
        S430 = newdecoder[23]; data["430"] = S430
        S431 = newdecoder[24]; data["431"] = S431
        S432 = newdecoder[25]; data["432"] = S432
        S433 = newdecoder[26]; data["433"] = S433
        S434 = newdecoder[27]; data["434"] = S434
        S435 = newdecoder[28]; data["435"] = S435
        S436 = newdecoder[29]; data["436"] = S436
        S437 = newdecoder[30]; data["437"] = S437
        S438 = newdecoder[31]; data["438"] = S438
        S439 = newdecoder[32]; data["439"] = S439
        S440 = newdecoder[33]; data["440"] = S440
        S441 = newdecoder[34]; data["441"] = S441
        S442 = newdecoder[35]; data["442"] = S442
        S443 = newdecoder[36]; data["443"] = S443
        S444 = newdecoder[37]; data["444"] = S444
        S445 = newdecoder[38]; data["445"] = S445
        S446 = newdecoder[39]; data["446"] = S446
        S447 = newdecoder[40]; data["447"] = S447
        S448 = newdecoder[41]; data["448"] = S448
        S449 = newdecoder[42]; data["449"] = S449
        S450 = newdecoder[43]; data["450"] = S450
        S451 = newdecoder[44]; data["450"] = S451
        S452 = newdecoder[45]; data["452"] = S452
        S453 = newdecoder[46]; data["453"] = S453
        S454 = newdecoder[47]; data["454"] = S454
        S455 = newdecoder[48]; data["455"] = S455
        S456 = newdecoder[49]; data["456"] = S456
        S457 = newdecoder[50]; data["457"] = S457
        S458 = newdecoder[51]; data["458"] = S458
        S459 = newdecoder[52]; data["459"] = S459

        return data

    def read_modbus_realtime_data(self) -> dict: # 499 t/m 539
        """Read the reatime sensor values"""
        realtime_data = self._read_holding_registers(unit=1, address=499, count=41)

        if realtime_data.isError():
            return {}

        data = {}
        newdecoder = ModbusTcpClient.convert_from_registers(realtime_data.registers, data_type=ModbusTcpClient.DATATYPE.INT16)

        mode = newdecoder[0]
        _mode = []
        _mode.extend(self.translate_mode_code_to_messages(mode, CURRENT_MODE.items()))
        data["499"] = ", ".join(_mode).strip()[0:254]

        S500 = newdecoder[1]
        if S500 in LOGIN_STATUS:
            data["500"] = LOGIN_STATUS[S500]

        S501 = newdecoder[2]; data["501"] = round(S501 * 0.01,2)
        S502 = newdecoder[3]; data["502"] = S502
        S503 = newdecoder[4]; data["503"] = round(S503 * 0.01, 2)
        S504 = newdecoder[5]; data["504"] = round(S504 * 0.01, 2)
        S505 = newdecoder[6]; data["505"] = round(S505 * 0.1, 2)
        S506 = newdecoder[7]; data["506"] = round(S506 * 0.1, 2)
        S507 = newdecoder[8]; data["507"] = round(S507 * 0.1, 2)
        S508 = newdecoder[9]; data["508"] = round(S508 * 0.1, 2)
        S509 = newdecoder[10]; data["509"] = round(S509 * 0.1, 2)
        S510 = newdecoder[11]; data["510"] = round(S510 * 0.1, 2)
        S511 = newdecoder[12]; data["511"] = round(S511 * 0.1, 2)
        S512 = newdecoder[13]; data["512"] = S512
        S513 = newdecoder[14]; data["513"] = S513

        S514 = newdecoder[15]
        if S514 in CURRENT_OPERATION_MODE:
            data["514"] = CURRENT_OPERATION_MODE[S514]

        S515 = newdecoder[16]; data["515"] = S515
        S516 = newdecoder[17]; data["516"] = S516
        S517 = newdecoder[18]; data["517"] = round(S517 * 0.1, 2)
        S518 = newdecoder[19]; data["518"] = round(S518 * 0.1, 2)
        S519 = newdecoder[20]; data["519"] = round(S519 * 0.1, 2)
        S520 = newdecoder[21]; data["520"] = round(S520 * 0.1, 2)
        S521 = newdecoder[22]; data["521"] = round(S521 * 0.1, 2)
        S522 = newdecoder[23]; data["522"] = round(S522 * 0.1, 2)
        S523 = newdecoder[24]; data["523"] = round(S523 * 0.1, 2)
        S524 = newdecoder[25]; data["524"] = round(S524 * 0.1, 2)
        S525 = newdecoder[26]; data["525"] = round(S525 * 0.1, 2)
        S526 = newdecoder[27]; data["526"] = S526
        S527 = newdecoder[28]; data["527"] = S527
        S528 = newdecoder[29]; data["528"] = round(S528 * 0.1, 2)
        S529 = newdecoder[30]; data["529"] = S529

        S530 = newdecoder[31]
        if S530 in ON_OFF_STATUS:
            data["530"] = ON_OFF_STATUS[S530]

        S531 = newdecoder[32]; data["531"] = round(S531 * 0.1, 2)

        S532 = newdecoder[33]
        if S532 in ON_OFF_STATUS:
            data["532"] = ON_OFF_STATUS[S532]

        S533 = newdecoder[34]
        if S533 in ON_OFF_STATUS:
            data["533"] = ON_OFF_STATUS[S533]

        S534 = newdecoder[35]
        if S534 in ON_OFF_STATUS:
            data["534"] = ON_OFF_STATUS[S534]
        
        S535 = newdecoder[36]
        if S535 in ON_OFF_STATUS:
            data["535"] = ON_OFF_STATUS[S535]

        S536 = newdecoder[37]
        if S536 in ON_OFF_STATUS:
            data["536"] = ON_OFF_STATUS[S536]

        S537 = newdecoder[38]; data["537"] = round(S537 * 0.1)
        S538 = newdecoder[39]; data["538"] = round(S538 * 0.1, 2)
        S539 = newdecoder[40]; data["539"] = round(S539 * 0.1, 2)

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
     