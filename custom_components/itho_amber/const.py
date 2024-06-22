"""Constants for the Amber integration."""

from dataclasses import dataclass
from homeassistant.components.switch import (
    SwitchEntity, 
    SwitchEntityDescription,
    SwitchDeviceClass,
)
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
    SensorEntityDescription,

)
from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
)

from homeassistant.components.select import (
    SelectEntityDescription,
    SelectEntity,     
)

from homeassistant.const import (
    UnitOfFrequency,
    UnitOfTemperature,
    UnitOfPressure,
    UnitOfTime,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,    
)

DOMAIN = "itho_amber"
DEFAULT_NAME = "Amber"
DEFAULT_PORT = 502
DEFAULT_SCAN_INTERVAL = 10
CONF_AMBER_HUB = "amber_hub"
ATTR_MANUFACTURER = "Amber by @remmob"
DEFAULT_ID = 1

ON_OFF_STATUS = {
    0: "OFF",
    1: "ON",
}

LOGIN_STATUS = {
    0: "User level",
    1: "Installer level",
    2: "Factory level"
}

CURRENT_MODE = {
    0x1: "DHW",    
    0x2: "Heating",
    0x4: "Cooling",
    0x8: "DHW in progress",
    0x10: "Heating in progress",
    0x20: "Cooling in progress",
    0x40: "timer in progress"
} 

CURRENT_OPERATION_MODE = {
    0: "Standby",
    1: "Heating",
    2: "Cooling",
    3: "test" 
} 

EXTERNAL_CONTROL = {
    0: "Off",
    1: "Outside temperture",
    2: "Ext. On/Off",
    3: "Ext. On/Off + Outside temperture" 
}

CURRENT_WORKING_MODE = { 
    0: "Standby",
    1: "Heating",
    2: "Cooling",
    3: "DHW",
    4: "Auto"
}

PUMP_SPEED = {
    0: "High",
    1: "Medium",
    2: "Low"
}

PUMP_P0_WORKING_MODE = {
    0: "interval",
    1: "on demand",
    2: "with compressor"
}

PUMP_TYPE = {
    0: "PWM",
    1: "AC"
}

MODE_SIGNAL_OUTPUT = {
    0: "No output",
    1: "Heating output",
    2: "Cooling output"
}

MODE_SIGNAL_TYPE = {
    0: "Normally Closed",
    1: "Normally Open",
    2: "Cooling Output"
}

HWTBH_PRIORITY_MODE = {
    0: "Internal (AH)",
    1: "External"
}

DISPLAY_TIME = {
    0: "Altijd",
    1: "3 min.",
    2: "5 min.",
    3: "10 min"
}

@dataclass
class AmberModbusSensorEntityDescription(SensorEntityDescription):
    """Amber sensor entities."""

SENSOR_TYPES: dict[str, list[AmberModbusSensorEntityDescription]] = {
    #Settings data
    "9": AmberModbusSensorEntityDescription(
        name="room temperture sensor",
        key="9",
        icon="mdi:toggle-switch-off-outline",
        entity_registry_enabled_default=True,
    ),
    "18": AmberModbusSensorEntityDescription(
        name="timer heating and cooling",
        key="18",
        icon="mdi:clock-outline",
        entity_registry_enabled_default=True,
    ),
    "31": AmberModbusSensorEntityDescription(
        name="Heatcurve outside temperture 1",
        key="31",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "32": AmberModbusSensorEntityDescription(
        name="Heatcurve outside temperture 2",
        key="32",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "33": AmberModbusSensorEntityDescription(
        name="Heatcurve outside temperture 3",
        key="33",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "34": AmberModbusSensorEntityDescription(
        name="Heatcurve outside temperture 4",
        key="34",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "35": AmberModbusSensorEntityDescription(
        name="Heatcurve outside temperture 5",
        key="35",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "36": AmberModbusSensorEntityDescription(
        name="Heatcurve-1 setpoint-1",
        key="36",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "37": AmberModbusSensorEntityDescription(
        name="Heatcurve-1 setpoint-2",
        key="37",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "38": AmberModbusSensorEntityDescription(
        name="Heatcurve-1 setpoint-3",
        key="38",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "39": AmberModbusSensorEntityDescription(
        name="Heatcurve-1 setpoint-4",
        key="39",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "40": AmberModbusSensorEntityDescription(
        name="Heatcurve-1 setpoint-5",
        key="40",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "42": AmberModbusSensorEntityDescription(
        name="Ideal room temp inheating",
        key="42",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "43": AmberModbusSensorEntityDescription(
        name="Ideal room temp incooling",
        key="43",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "49": AmberModbusSensorEntityDescription(
        name="legionella setpoint",
        key="49",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "50": AmberModbusSensorEntityDescription(
        name="legionella duration",
        key="50",
        icon="mdi:timer-outline",
        native_unit_of_measurement="Min",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "51": AmberModbusSensorEntityDescription(
        name="legionella max elapsed time",
        key="51",
        icon="mdi:timer-outline",
        native_unit_of_measurement="Min",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "62": AmberModbusSensorEntityDescription(
        name="temperture rise interval hwtbh",
        key="62",
        icon="mdi:timer-outline",
        native_unit_of_measurement="Min",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "66": AmberModbusSensorEntityDescription(
        name="shifting priority dhw",
        key="66",
        icon="mdi:toggle-switch-off-outline",
        entity_registry_enabled_default=True,
    ),
    "67": AmberModbusSensorEntityDescription(
        name="shifting priority dhw temperture",
        key="67",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "68": AmberModbusSensorEntityDescription(
        name="min heating time dhw",
        key="68",
        icon="mdi:timer-outline",
        native_unit_of_measurement="Min",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "69": AmberModbusSensorEntityDescription(
        name="max cv heating time in dhw mode",
        key="69",
        icon="mdi:timer-outline",
        native_unit_of_measurement="Min",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "70": AmberModbusSensorEntityDescription(
        name="shifting priority temperture diff",
        key="70",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "71": AmberModbusSensorEntityDescription(
        name="backup heater shifting priority",
        key="71",
        icon="mdi:toggle-switch-off-outline",
        entity_registry_enabled_default=True,
    ),
    "73": AmberModbusSensorEntityDescription(
        name="min temperture timer dhw",
        key="73",
        icon="mdi:toggle-switch-off-outline",
        entity_registry_enabled_default=True,
    ),
    "74": AmberModbusSensorEntityDescription(
        name="min temperture setpoint dhw",
        key="74",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "75": AmberModbusSensorEntityDescription(
        name="restart min temperture dhw",
        key="75",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "93": AmberModbusSensorEntityDescription(
        name="Heatcurve-2 setpoint-1",
        key="93",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "94": AmberModbusSensorEntityDescription(
        name="Heatcurve-2 setpoint-2",
        key="94",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "95": AmberModbusSensorEntityDescription(
        name="Heatcurve-2 setpoint-3",
        key="95",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "96": AmberModbusSensorEntityDescription(
        name="Heatcurve-2 setpoint-4",
        key="96",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "97": AmberModbusSensorEntityDescription(
        name="Heatcurve-2 setpoint-5",
        key="97",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "119": AmberModbusSensorEntityDescription(
        name="cv contact",
        key="119",
        icon="mdi:gas-burner",
        entity_registry_enabled_default=True,
    ),
    "121": AmberModbusSensorEntityDescription(
        name="hbh during electrical utility lock",
        key="121",
        icon="mdi:flash-triangle-outline",
        entity_registry_enabled_default=True,
    ),
    "122": AmberModbusSensorEntityDescription(
        name="P0 active during external heating",
        key="122",
        icon="mdi:pump",
        entity_registry_enabled_default=True,
    ),
    "126": AmberModbusSensorEntityDescription(
        name="system display on time",
        key="126",
        icon="mdi:timer-outline",
        entity_registry_enabled_default=True,
    ),
    "137": AmberModbusSensorEntityDescription(
        name="P0 type",
        key="137",
        icon="mdi:pump",
        entity_registry_enabled_default=True,
    ),
    "143": AmberModbusSensorEntityDescription(
        name="Mixing valve zone 1",
        key="143",
        icon="mdi:toggle-switch-off-outline",
        entity_registry_enabled_default=True,
    ),
    "144": AmberModbusSensorEntityDescription(
        name="mixing valve zone 2",
        key="144",
        icon="mdi:toggle-switch-off-outline",
        entity_registry_enabled_default=True,
    ),
    "145": AmberModbusSensorEntityDescription(
        name="P1 heating",
        key="145",
        icon="mdi:pump",
        entity_registry_enabled_default=True,
    ),
    "146": AmberModbusSensorEntityDescription(
        name="P1 cooling",
        key="146",
        icon="mdi:pump",
        entity_registry_enabled_default=True,
    ),
    "147": AmberModbusSensorEntityDescription(
        name="P1 high demand",
        key="147",
        icon="mdi:pump",
        entity_registry_enabled_default=True,
    ),
    "148": AmberModbusSensorEntityDescription(
        name="P2 heating",
        key="148",
        icon="mdi:pump",
        entity_registry_enabled_default=True,
    ),
    "149": AmberModbusSensorEntityDescription(
        name="P2 cooling",
        key="149",
        icon="mdi:pump",
        entity_registry_enabled_default=True,
    ),
    "150": AmberModbusSensorEntityDescription(
        name="P2 high demand",
        key="150",
        icon="mdi:pump",
        entity_registry_enabled_default=True,
    ),
    "158": AmberModbusSensorEntityDescription(
        name="outside start temperture frost protection first stage",
        key="158",
        icon="mdi:snowflake-thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "159": AmberModbusSensorEntityDescription(
        name="outside start temperture frost protection second stage",
        key="159",
        icon="mdi:snowflake-thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "160": AmberModbusSensorEntityDescription(
        name="outside stop temperture frost protection first stage",
        key="160",
        icon="mdi:snowflake-thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "161": AmberModbusSensorEntityDescription(
        name="water start temperture frost protection second stage",
        key="161",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "162": AmberModbusSensorEntityDescription(
        name="water stop temperture frost protection second stage",
        key="162",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "189": AmberModbusSensorEntityDescription(
        name="fan speed limit",
        key="189",
        icon="mdi:fan",
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "202": AmberModbusSensorEntityDescription(
        name="mode signal output",
        key="202",
        icon="mdi:toggle-switch-off-outline",
        entity_registry_enabled_default=True,
    ),
    "203": AmberModbusSensorEntityDescription(
        name="mode signal type",
        key="203",
        icon="mdi:toggle-switch-off-outline",
        entity_registry_enabled_default=True,
    ),
    "218": AmberModbusSensorEntityDescription(
        name="block external heating on outsidetemperture",
        key="218",
        icon="mdi:toggle-switch-off-outline",
        entity_registry_enabled_default=True,
    ),
    "219": AmberModbusSensorEntityDescription(
        name="setpoint block external heating on outsidetemperture",
        key="219",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),

    "314": AmberModbusSensorEntityDescription(
        name="coolcurve outside temperture 1",
        key="314",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "315": AmberModbusSensorEntityDescription(
        name="coolcurve outside temperture 2",
        key="315",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "316": AmberModbusSensorEntityDescription(
        name="coolcurve outside temperture 3",
        key="316",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "317": AmberModbusSensorEntityDescription(
        name="coolcurve 1 setpoint 1",
        key="317",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "318": AmberModbusSensorEntityDescription(
        name="coolcurve 1 setpoint 2",
        key="318",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "319": AmberModbusSensorEntityDescription(
        name="coolcurve 1 setpoint 3",
        key="319",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "323": AmberModbusSensorEntityDescription(
        name="coolcurve zone 1",
        key="323",
        icon="mdi:chart-line",
        entity_registry_enabled_default=True,
    ),
    "320": AmberModbusSensorEntityDescription(
        name="coolcurve 2 setpoint 1",
        key="320",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "321": AmberModbusSensorEntityDescription(
        name="coolcurve 2 setpoint 2",
        key="321",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "322": AmberModbusSensorEntityDescription(
        name="coolcurve 2 setpoint 3",
        key="322",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "324": AmberModbusSensorEntityDescription(
        name="coolcurve zone 2",
        key="324",
        icon="mdi:chart-line",
        entity_registry_enabled_default=True,
    ),
    "339": AmberModbusSensorEntityDescription(
        name="sg ready",
        key="339",
        icon="mdi:transmission-tower-export",
        entity_registry_enabled_default=True,
    ),
    "340": AmberModbusSensorEntityDescription(
        name="sg increase setpoint heating",
        key="340",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "375": AmberModbusSensorEntityDescription(
        name="sg increase setpoint dhw",
        key="375",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "376": AmberModbusSensorEntityDescription(
        name="sg decrease setrpoint cooling",
        key="376",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    # Realtime Sensor data
    "499": AmberModbusSensorEntityDescription(
        name="Current working mode",
        key="499",
        icon="mdi:auto-mode",
    ),
    "500": AmberModbusSensorEntityDescription(
        name="System login status",
        key="500",
        icon="mdi:account",
    ),
    "501": AmberModbusSensorEntityDescription(
        name="Software version",
        key="501",
        icon="mdi:database-outline",
    ),
    "503": AmberModbusSensorEntityDescription(
        name="Database version",
        key="503",
        icon="mdi:database-outline",
    ),
    "504": AmberModbusSensorEntityDescription(
        name="Software version outdoor unit",
        key="504",
        icon="mdi:database-outline",
    ),
    "505": AmberModbusSensorEntityDescription(
        name="water outlet temperature (TUO)",
        key="505",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "506": AmberModbusSensorEntityDescription(
        name="water inlet temperature (TUI)",
        key="506",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "507": AmberModbusSensorEntityDescription(
        name="Condenser temperture (TUP)",
        key="507",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "508": AmberModbusSensorEntityDescription(
        name="DHW temperture (TW)",
        key="508",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "509": AmberModbusSensorEntityDescription(
        name="Heating/Cooling watertemperture (TC)",
        key="509",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "510": AmberModbusSensorEntityDescription(
        name="Heating/Cooling zone 1 watertemperture (TV1)",
        key="510",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "511": AmberModbusSensorEntityDescription(
        name="Heating/Cooling zone 2 watertemperture (TV2)",
        key="511",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "514": AmberModbusSensorEntityDescription(
        name="Current operating mode",
        key="514",
        icon="mdi:auto-mode",
    ),
    "515": AmberModbusSensorEntityDescription(
        name="Compressor speed",
        key="515",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "516": AmberModbusSensorEntityDescription(
        name="EEV opening",
        key="516",
        icon="mdi:sine-wave",
    ),
    "517": AmberModbusSensorEntityDescription(
        name="Ambient temperture (TA)",
        key="517",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "518": AmberModbusSensorEntityDescription(
        name="1h Average ambient temperture",
        key="518",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "519": AmberModbusSensorEntityDescription(
        name="4h Average ambient temperture",
        key="519",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "520": AmberModbusSensorEntityDescription(
        name="24h Average ambient temperture",
        key="520",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "521": AmberModbusSensorEntityDescription(
        name="Compressor high pressure",
        key="521",
        native_unit_of_measurement = UnitOfPressure.BAR,
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "522": AmberModbusSensorEntityDescription(
        name="Compressor low pressure",
        key="522",
        native_unit_of_measurement = UnitOfPressure.BAR,
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "523": AmberModbusSensorEntityDescription(
        name="Compressor discharge temperture",
        key="523",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "524": AmberModbusSensorEntityDescription(
        name="Compressor suction temperture",
        key="524",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "525": AmberModbusSensorEntityDescription(
        name="Coil temperture (TP)",
        key="525",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "526": AmberModbusSensorEntityDescription(
        name="Fan speed",
        key="526",
        icon="mdi:fan",
        native_unit_of_measurement="RPM",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "528": AmberModbusSensorEntityDescription(
        name="Running Current",
        key="528",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "529": AmberModbusSensorEntityDescription(
        name="Supply Voltage",
        key="529",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "530": AmberModbusSensorEntityDescription(
        name="Defrost status",
        key="530",
        icon="mdi:snowflake",
        entity_registry_enabled_default=True,
    ),    
    "531": AmberModbusSensorEntityDescription(
        name="Room temperture (TR)",
        key="531",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "532": AmberModbusSensorEntityDescription(
        name="Flow switch",
        key="532",
        icon="mdi:waves",
        entity_registry_enabled_default=True,
    ),
    "533": AmberModbusSensorEntityDescription(
        name="Electrical utility lock",
        key="533",
        icon="mdi:toggle-switch-off-outline",
        entity_registry_enabled_default=True,
    ),
    "534": AmberModbusSensorEntityDescription(
        name="External cooling signal (CS)",
        key="534",
        icon="mdi:toggle-switch-off-outline",
        entity_registry_enabled_default=True,
    ),
    "535": AmberModbusSensorEntityDescription(
        name="External heating signal (HS)",
        key="535",
        icon="mdi:toggle-switch-off-outline",
        entity_registry_enabled_default=True,
    ),
    "536": AmberModbusSensorEntityDescription(
        name="External high demand signal (HD)",
        key="536",
        icon="mdi:toggle-switch-off-outline",
        entity_registry_enabled_default=True,
    ),
    "537": AmberModbusSensorEntityDescription(
        name="PWM waterpump signal",
        key="537",
        icon="mdi:pump",
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "538": AmberModbusSensorEntityDescription(
        name="Mixing valve 1 ouputsignal",
        key="538",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "539": AmberModbusSensorEntityDescription(
        name="Mixing valve 2 ouputsignal",
        key="539",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
}

@dataclass
class AmberModbusNumberEntityDescription(NumberEntityDescription):
    """Amber number entities."""

NUMBER_TYPES: dict[str, list[AmberModbusNumberEntityDescription]] = {
    # Writeble sensor values (numbers)
    "10": AmberModbusNumberEntityDescription(
        name="outside temperture start heating",
        key= "10",
        mode="slider",
        native_min_value= -10,
        native_max_value= 25, 
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "11": AmberModbusNumberEntityDescription(
        name="outside temperture start cooling",
        key= "11",
        mode="slider",
        native_min_value= 20,
        native_max_value= 53, 
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "12": AmberModbusNumberEntityDescription(
        name="duration min compressor speed",
        key= "12",
        mode="slider",
        native_min_value= 5,
        native_max_value= 180,
        icon="mdi:timer-outline", 
        native_unit_of_measurement="Min",
        entity_registry_enabled_default=True,
    ),
    "26": AmberModbusNumberEntityDescription(
        name="heating and cooling stop",
        key= "26",
        mode="slider",
        native_min_value= 1,
        native_max_value= 5,
        icon="mdi:water-thermometer-outline", 
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "27": AmberModbusNumberEntityDescription(
        name="heating and cooling restart",
        key= "27",
        mode="slider",
        native_min_value= 1,
        native_max_value= 10,
        icon="mdi:water-thermometer-outline", 
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "28": AmberModbusNumberEntityDescription(
        name="compressor speed reduction",
        key= "28",
        mode="slider",
        native_min_value= 1,
        native_max_value= 10,
        icon="mdi:water-thermometer-outline", 
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "29": AmberModbusNumberEntityDescription(
        name="Cooling-1 setpoint",
        key="29",
        mode="slider",
        native_min_value= 12,
        native_max_value= 25,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "44": AmberModbusNumberEntityDescription(
        name="zone 1 heating setpoint",
        key="44",
        mode="slider",
        native_min_value= 20,
        native_max_value= 55,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "45": AmberModbusNumberEntityDescription(
        name="max setpoint setting zone 1",
        key="45",
        mode="slider",
        native_min_value= 20,
        native_max_value= 55,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "46": AmberModbusNumberEntityDescription(
        name="min setpoint setting zone 1",
        key="46",
        mode="slider",
        native_min_value= 1,
        native_max_value= 50,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "54": AmberModbusNumberEntityDescription(
        name="room temperture vacation mode",
        key="54",
        mode="slider",
        native_min_value= 1,
        native_max_value= 50,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "53": AmberModbusNumberEntityDescription(
        name="restart dhw vacation mode",
        key="53",
        mode="slider",
        native_min_value= 25,
        native_max_value= 70,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "61": AmberModbusNumberEntityDescription(
        name="delay hbh",
        key= "61",
        mode="slider",
        native_min_value= 0,
        native_max_value= 600,
        icon="mdi:timer-outline", 
        native_unit_of_measurement="Min",
        entity_registry_enabled_default=True,
    ),
    "64": AmberModbusNumberEntityDescription(
        name="setpoint dhw",
        key="64",
        mode="slider",
        native_min_value= 25,
        native_max_value=70,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "65": AmberModbusNumberEntityDescription(
        name="restart dhw",
        key="65",
        mode="slider",
        native_min_value= 2,
        native_max_value= 15,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "91": AmberModbusNumberEntityDescription(
        name="zone 2 cooling setpoint",
        key="91",
        mode="slider",
        native_min_value= 7,
        native_max_value= 25,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "98": AmberModbusNumberEntityDescription(
        name="zone 2 heating setpoint",
        key="98",
        mode="slider",
        native_min_value= 20,
        native_max_value= 55,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "99": AmberModbusNumberEntityDescription(
        name="max setpoint setting zone 2",
        key="99",
        mode="slider",
        native_min_value= 20,
        native_max_value= 75,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "100": AmberModbusNumberEntityDescription(
        name="min setpoint setting zone 2",
        key="100",
        mode="slider",
        native_min_value= 7,
        native_max_value= 25,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "102": AmberModbusNumberEntityDescription(
        name="reduced mode setpoint",
        key="102",
        mode="slider",
        native_min_value= 2,
        native_max_value= 10,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "111": AmberModbusNumberEntityDescription(
        name="reduced mode delta",
        key="111",
        mode="slider",
        native_min_value= 2,
        native_max_value= 10,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "133": AmberModbusNumberEntityDescription(
        name="outsidetemperture start dhw eco mode",
        key="133",
        mode="slider",
        native_min_value= -20,
        native_max_value= 43,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "134": AmberModbusNumberEntityDescription(
        name="outside temperture start external heating",
        key="134",
        mode="slider",
        native_min_value= -20,
        native_max_value= 43,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "140": AmberModbusNumberEntityDescription(
        name="P0_off_interval",
        key= "140",
        mode="slider",
        native_min_value= 5,
        native_max_value= 60,
        icon="mdi:timer-outline", 
        native_unit_of_measurement="Min",
        entity_registry_enabled_default=True,
    ),
    "141": AmberModbusNumberEntityDescription(
        name="P0_run_interval",
        key= "141",
        mode="slider",
        native_min_value= 1,
        native_max_value= 10,
        icon="mdi:timer-outline", 
        native_unit_of_measurement="Min",
        entity_registry_enabled_default=True,
    ),
    "175": AmberModbusNumberEntityDescription(
        name="3way valve switching time",
        key= "175",
        mode="slider",
        native_min_value= 1,
        native_max_value= 16,
        icon="mdi:timer-outline", 
        native_unit_of_measurement="Min",
        entity_registry_enabled_default=True,
    ),
    "176": AmberModbusNumberEntityDescription(
        name="3way valve power mode",
        key= "176",
        mode="slider",
        native_min_value= 0,
        native_max_value= 16,
        icon="mdi:timer-outline", 
        native_unit_of_measurement="Min",
        entity_registry_enabled_default=True,
    ),
}

@dataclass
class AmberModbusSwitchEntityDescription(SwitchEntityDescription):
    """Amber switch entities."""

SWITCH_TYPES: dict[str, list[AmberModbusSwitchEntityDescription]] = {
    #Switches
    "0": AmberModbusSwitchEntityDescription(
        name="Amber ON/OFF",
        key="0",
        icon="mdi:toggle-switch-off-outline",
        device_class=SwitchDeviceClass.SWITCH,
    ),
    "5": AmberModbusSwitchEntityDescription(
        name="dhw",
        key="5",
        icon="mdi:toggle-switch-off-outline",
        device_class=SwitchDeviceClass.SWITCH,
    ),
    "6": AmberModbusSwitchEntityDescription(
        name="heating",
        key="6",
        icon="mdi:toggle-switch-off-outline",
        device_class=SwitchDeviceClass.SWITCH,
    ),
    "7": AmberModbusSwitchEntityDescription(
        name="cooling",
        key="7",
        icon="mdi:toggle-switch-off-outline",
        device_class=SwitchDeviceClass.SWITCH,
    ),
    "30": AmberModbusSwitchEntityDescription(
        name="Heat Curve zone 1",
        key="30",
        icon="mdi:chart-line",
        device_class=SwitchDeviceClass.SWITCH
    ),
    "41": AmberModbusSwitchEntityDescription(
        name="Heat curve 1 correction",
        key="41",
        icon="mdi:chart-line",
        device_class=SwitchDeviceClass.SWITCH,
    ),
    "47": AmberModbusSwitchEntityDescription(
        name="legionella mode",
        key="47",
        icon="mdi:chart-line",
        device_class=SwitchDeviceClass.SWITCH,
    ),
    "52": AmberModbusSwitchEntityDescription(
        name="vacation mode",
        key="52",
        icon="mdi:calendar-clock-outline",
        device_class=SwitchDeviceClass.SWITCH,
    ),
    "59": AmberModbusSwitchEntityDescription(
        name="hwtbh",
        key="59",
        icon="mdi:toggle-switch-off-outline",
        device_class=SwitchDeviceClass.SWITCH,
    ),
    "63": AmberModbusSwitchEntityDescription(
        name="allow emergency heating",
        key="63",
        icon="mdi:radiator",
        device_class=SwitchDeviceClass.SWITCH,
    ),
    "72": AmberModbusSwitchEntityDescription(
        name="timer dhw",
        key="72",
        icon="mdi:clock-outline",
        device_class=SwitchDeviceClass.SWITCH,
    ),
    "90": AmberModbusSwitchEntityDescription(
        name="temperture zone 2",
        key="90",
        icon="mdi:home-thermometer-outline",
        device_class=SwitchDeviceClass.SWITCH,
    ),
    "92": AmberModbusSwitchEntityDescription(
        name="Heat Curve zone 2",
        key="92",
        icon="mdi:chart-line",
        device_class=SwitchDeviceClass.SWITCH,
    ),
    "101": AmberModbusSwitchEntityDescription(
        name="reduced mode",
        key="101",
        icon="mdi:volume-off",
        device_class=SwitchDeviceClass.SWITCH,
    ),
    "110": AmberModbusSwitchEntityDescription(
        name="timer reduced mode",
        key="110",
        icon="mdi:clock-outline",
        device_class=SwitchDeviceClass.SWITCH,
    ),
    "135": AmberModbusSwitchEntityDescription(
        name="dhw eco mode",
        key="135",
        icon="mdi:sprout",
        device_class=SwitchDeviceClass.SWITCH,
    ),
    "136": AmberModbusSwitchEntityDescription(
        name="external heating allowed",
        key="136",
        icon="mdi:gas-burner",
        device_class=SwitchDeviceClass.SWITCH,
    ),
    "142": AmberModbusSwitchEntityDescription(
        name="buffer tank",
        key="142",
        icon="mdi:water-boiler",
        device_class=SwitchDeviceClass.SWITCH,
    ),
    "217": AmberModbusSwitchEntityDescription(
        name="block external heating",
        key="217",
        icon="mdi:radiator-off",
        device_class=SwitchDeviceClass.SWITCH,
    ),
}

@dataclass
class AmberModbusSelectEntityControlDescription(SelectEntityDescription):
    """Amber select entities."""

SELECT_CONTROL: dict[str, list[AmberModbusSelectEntityControlDescription]] = {
    
    "8": AmberModbusSelectEntityControlDescription(
        name="Control mode",
        key="8",
        icon="mdi:menu-open",
        entity_registry_enabled_default=True,
    ),
}

@dataclass
class AmberModbusSelectEntityWorkingDescription(SelectEntityDescription):
    """Amber select working mode entities."""

SELECT_WORKING: dict[str, list[AmberModbusSelectEntityWorkingDescription]] = {
    
    "3": AmberModbusSelectEntityWorkingDescription(
        name="Working mode",
        key="3",
        icon="mdi:menu-open",
        entity_registry_enabled_default=True,
    ),
} 

@dataclass
class AmberModbusSelectEntityHWTBHPriorityDescription(SelectEntityDescription):
    """Amber select HWTBH Priority entities."""

SELECT_HWTBH: dict[str, list[AmberModbusSelectEntityHWTBHPriorityDescription]] = { 

    "60": AmberModbusSelectEntityHWTBHPriorityDescription(
        name="hwtbh priority",
        key="60",
        icon="mdi:menu-open",
        entity_registry_enabled_default=True,
    ),
}

@dataclass
class AmberModbusSelectEntityP0PumpModeDescription(SelectEntityDescription):
    """Amber select P0 Pump Mode entities."""

SELECT_PUMP_P0_WORKING_MODE: dict[str, list[AmberModbusSelectEntityP0PumpModeDescription]] = { 

    "139": AmberModbusSelectEntityP0PumpModeDescription(
        name="P0 working mode",
        key="139",
        icon="mdi:menu-open",
        entity_registry_enabled_default=True,
    ),
}

@dataclass
class AmberModbusSelectEntityP0PumpSpeedDescription(SelectEntityDescription):
    """Amber select P0 Pump speed entities."""

SELECT_PUMP_P0_SPEED: dict[str, list[AmberModbusSelectEntityP0PumpSpeedDescription]] = { 

    "214": AmberModbusSelectEntityP0PumpSpeedDescription(
        name="P0 speed heating",
        key="214",
        icon="mdi:pump",
        entity_registry_enabled_default=True,
    ),
    "215": AmberModbusSelectEntityP0PumpSpeedDescription(
        name="P0 speed cooling",
        key="215",
        icon="mdi:pump",
        entity_registry_enabled_default=True,
    ),
    "216": AmberModbusSelectEntityP0PumpSpeedDescription(
        name="P0 speed dhw",
        key="216",
        icon="mdi:pump",
        entity_registry_enabled_default=True,
    ),

}