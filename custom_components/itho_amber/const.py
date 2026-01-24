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
from homeassistant.helpers.entity import EntityCategory
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
DEFAULT_NAME = "Itho Amber 65/95/120 Heatpump integration"
DEFAULT_PORT = 502
DEFAULT_SCAN_INTERVAL = 10
CONF_AMBER_HUB = "amber_hub"
ATTR_MANUFACTURER = "Mischa Bommer"
ATTR_COPYRIGHT = "©2026 Bommer Software"

# Notification configuration - Alarms (P/F/E/S)
CONF_NOTIFY_ALARMS_MOBILE = "notify_alarms_mobile"
CONF_NOTIFY_ALARMS_PERSISTENT = "notify_alarms_persistent"
CONF_NOTIFY_ALARMS_SERVICES = "notify_alarms_services"
CONF_ALARM_NOTIFICATION_TITLE = "alarm_notification_title"
CONF_ALARM_DELAY = "alarm_delay"

# Notification configuration - Connection/Integration errors
CONF_NOTIFY_CONNECTION_ERRORS_MOBILE = "notify_connection_errors_mobile"
CONF_NOTIFY_CONNECTION_ERRORS_PERSISTENT = "notify_connection_errors_persistent"
CONF_NOTIFY_CONNECTION_ERRORS_SERVICES = "notify_connection_errors_services"
CONF_CONNECTION_ERROR_NOTIFICATION_TITLE = "connection_error_notification_title"
CONF_CONNECTION_ERROR_DELAY = "connection_error_delay"

# Backwards compatibility (deprecated)
CONF_NOTIFY_CONNECTION_ERRORS = "notify_connection_errors"
CONF_NOTIFY_PARTIAL_FAILURES = "notify_partial_failures"
CONF_NOTIFY_PARTIAL_FAILURES_MOBILE = "notify_partial_failures_mobile"
CONF_NOTIFY_ALARMS = "notify_alarms"
CONF_NOTIFY_SERVICES = "notify_services"

# Default values
DEFAULT_NOTIFY_ALARMS_MOBILE = False
DEFAULT_NOTIFY_ALARMS_PERSISTENT = False
DEFAULT_NOTIFY_ALARMS_SERVICES = ""
DEFAULT_ALARM_NOTIFICATION_TITLE = "Warmtepomp in storing!"
DEFAULT_ALARM_DELAY = 60

DEFAULT_NOTIFY_CONNECTION_ERRORS_MOBILE = False
DEFAULT_NOTIFY_CONNECTION_ERRORS_PERSISTENT = False
DEFAULT_NOTIFY_CONNECTION_ERRORS_SERVICES = ""
DEFAULT_CONNECTION_ERROR_NOTIFICATION_TITLE = "Warmtepomp verbindingsfout!"
DEFAULT_CONNECTION_ERROR_DELAY = 60

# Backwards compatibility defaults
DEFAULT_NOTIFY_CONNECTION_ERRORS = True
DEFAULT_CONNECTION_ERROR_DELAY = 60
DEFAULT_NOTIFY_PARTIAL_FAILURES = True
DEFAULT_NOTIFY_PARTIAL_FAILURES_MOBILE = False
DEFAULT_NOTIFY_ALARMS = False
DEFAULT_NOTIFY_SERVICES = ""
DEFAULT_ID = 1

# Alarm sensor keys to monitor
ALARM_SENSORS = [
    # P errors (1 minute delay)
    "p01_main_line_current_protection",
    "p02_compressor_phase_current_protection",
    "p03_ipm_module_protection",
    "p04_compresor_oil_return_protection",
    "p05_high_pressure_refrigerant_circuit",
    "p06_very_high_pressure_refrigerant_circuit",
    "p07_pre_heat_compressor",
    "p08_gas_discharge_temp_sensor_protection",
    "p09_evaporator_coil_temp_sensor_protection",
    "p10_main_voltage_protection",
    "p11_compressor_stop_ambient_temperature",
    "p12_frequency_limit_compressor",
    "p13_low_pressure_condensor_pressure_switch",
    # F errors (1 minute delay)
    "f01_failure_ambient_temperature_sensor_ta",
    "f02_failure_outdoor_temperature_sensor_tp",
    "f03_failure_compressor_discharge_temperature_sensor_tp",
    "f04_failure_compressor_suction_temperature_sensor_ts",
    "f05_failure_evporating_pressure_sensor_ps",
    "f06_failure_high_pressure_sensor_pd",
    "f07_failure_high_pressure_switch",
    "f09_failure_a_fan_motor",
    "f10_failure_b_fan_motor",
    "f11_evporating_pressure_failure_ps",
    "f12_high_pressure_failure_pd",
    "f13_room_temperature_sensor_failure_tr",
    "f14_failure_dhw_tank_temperature_sensor_tw",
    "f15_failure_temperature_control_sensor_tc",
    "f16_failure_outlet_temperature_sensor_tuo",
    "f17_failure_inlet_temperature_sensor_tui",
    "f18_failure_coil_temperature_sensor",
    "f21_failure_water_temperature_sensor_zone1_tv1",
    "f22_failure_water_temperature_sensor_zone2_tv2",
    "f25_communication_failure",
    "f27_failure_eeprom_indoor_unit",
    "f28_pwm_signal_failure_pomp_p0",
    "f29_failure_3_way_valve_zone1",
    "f30_failure_3_way_valve_zone2",
    # E errors (1 minute delay)
    "e01_comm_failure_lcd_indoorunit",
    "e02_failure_outdoor_pcb_compressor_inverter",
    "e03_power_failure_compressor",
    "e04_overcurrent_protection_compressor",
    "e05_compressor_driver_failure",
    "e06_vdc_unit_failure",
    "e07_ac_current_failure",
    "e08_eeprom_failure_oudoor_unit",
    # S errors (1 minute delay, except S06/S07 which need 5 minutes)
    "s01_cooling_anti_freezing_protection",
    "s02_low_flow_warning",
    "s03_flow_switch_failure",
    "s04_communication_failure_indoor_unit",
    "s05_communication_failure_outdoor_unit",
    "s06_water_outlet_to_low_in_cooling",
    "s07_water_outlet_to_high_in_heating",
    "s08_defrost_failure",
    "s09_water_outlet_temperature_low_during_defrost",
    "s10_flow_switch_failure",
    "s11_cooling_anti_freezing_protection",
    "s13_failure_4_way_valve",
]

ON_OFF_STATUS = {
    0: "OFF",
    1: "ON",
}

LOGIN_STATUS = {
    0: "User level",
    1: "Installer level",
    2: "Factory level"
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

FAILURE_STATUS = {
    0: "No Alarm",
    1: "ALARM"
}

ACTIVE_STATUS = {
    0: "Inactive",
    1: "Active"
}

@dataclass
class AmberModbusSensorEntityDescription(SensorEntityDescription):
    """Amber sensor entities."""
    native_min_value: float | None = None
    native_max_value: float | None = None

SENSOR_TYPES: dict[str, list[AmberModbusSensorEntityDescription]] = {
    #Settings data
    "9": AmberModbusSensorEntityDescription(
        name="room temperature sensor",
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
    "49": AmberModbusSensorEntityDescription(
        name="legionella setpoint",
        key="49",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "50": AmberModbusSensorEntityDescription(
        name="legionella duration",
        key="50",
        icon="mdi:timer-outline",
        native_unit_of_measurement="Min",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "51": AmberModbusSensorEntityDescription(
        name="legionella max elapsed time",
        key="51",
        icon="mdi:timer-outline",
        native_unit_of_measurement="Min",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "62": AmberModbusSensorEntityDescription(
        # Tijdsinterval tapwatertemperatuur ∆T=+1°C
        name="temperature rise interval hwtbh",
        key="62",
        icon="mdi:timer-outline",
        native_unit_of_measurement="Min",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "66": AmberModbusSensorEntityDescription(
        name="shifting priority dhw",
        key="66",
        icon="mdi:toggle-switch-off-outline",
        entity_registry_enabled_default=True,
    ),
    "67": AmberModbusSensorEntityDescription(
        name="shifting priority dhw temperature",
        key="67",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "68": AmberModbusSensorEntityDescription(
        name="min heating time dhw",
        key="68",
        icon="mdi:timer-outline",
        native_unit_of_measurement="Min",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "69": AmberModbusSensorEntityDescription(
        name="max cv heating time in dhw mode",
        key="69",
        icon="mdi:timer-outline",
        native_unit_of_measurement="Min",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "70": AmberModbusSensorEntityDescription(
        name="shifting priority temperature diff",
        key="70",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "71": AmberModbusSensorEntityDescription(
        name="backup heater shifting priority",
        key="71",
        icon="mdi:toggle-switch-off-outline",
        entity_registry_enabled_default=True,
    ),
    "73": AmberModbusSensorEntityDescription(
        name="min temperature timer dhw",
        key="73",
        icon="mdi:toggle-switch-off-outline",
        entity_registry_enabled_default=True,
    ),
    "74": AmberModbusSensorEntityDescription(
        name="min temperature setpoint dhw",
        key="74",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "75": AmberModbusSensorEntityDescription(
        name="restart min temperature dhw",
        key="75",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
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
        icon="mdi:pipe-valve",
        entity_registry_enabled_default=True,
    ),
    "144": AmberModbusSensorEntityDescription(
        name="mixing valve zone 2",
        key="144",
        icon="mdi:pipe-valve",
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
        name="outside start temperature frost protection first stage",
        key="158",
        icon="mdi:snowflake-thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "159": AmberModbusSensorEntityDescription(
        name="outside start temperature frost protection second stage",
        key="159",
        icon="mdi:snowflake-thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "160": AmberModbusSensorEntityDescription(
        name="outside stop temperature frost protection first stage",
        key="160",
        icon="mdi:snowflake-thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "161": AmberModbusSensorEntityDescription(
        name="water start temperature frost protection second stage",
        key="161",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "162": AmberModbusSensorEntityDescription(
        name="water stop temperature frost protection second stage",
        key="162",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "189": AmberModbusSensorEntityDescription(
        name="fan speed limit",
        key="189",
        icon="mdi:fan",
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
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
        name="block external heating on outsidetemperature",
        key="218",
        icon="mdi:toggle-switch-off-outline",
        entity_registry_enabled_default=True,
    ),
    "219": AmberModbusSensorEntityDescription(
        name="setpoint block external heating on outsidetemperature",
        key="219",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "314": AmberModbusSensorEntityDescription(
        name="coolcurve outside temperature 1",
        key="314",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "315": AmberModbusSensorEntityDescription(
        name="coolcurve outside temperature 2",
        key="315",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "316": AmberModbusSensorEntityDescription(
        name="coolcurve outside temperature 3",
        key="316",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "317": AmberModbusSensorEntityDescription(
        name="coolcurve 1 setpoint 1",
        key="317",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "318": AmberModbusSensorEntityDescription(
        name="coolcurve 1 setpoint 2",
        key="318",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "319": AmberModbusSensorEntityDescription(
        name="coolcurve 1 setpoint 3",
        key="319",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
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
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "321": AmberModbusSensorEntityDescription(
        name="coolcurve 2 setpoint 2",
        key="321",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "322": AmberModbusSensorEntityDescription(
        name="coolcurve 2 setpoint 3",
        key="322",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "324": AmberModbusSensorEntityDescription(
        name="coolcurve zone 2",
        key="324",
        icon="mdi:chart-line",
        entity_registry_enabled_default=True,
    ),
    "334": AmberModbusSensorEntityDescription(
        name="max dhw setpoint setting",
        key="334",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
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
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "375": AmberModbusSensorEntityDescription(
        name="sg increase setpoint dhw",
        key="375",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "376": AmberModbusSensorEntityDescription(
        name="sg decrease setrpoint cooling",
        key="376",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
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
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "506": AmberModbusSensorEntityDescription(
        name="water inlet temperature (TUI)",
        key="506",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "507": AmberModbusSensorEntityDescription(
        name="Condenser temperature (TUP)",
        key="507",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "508": AmberModbusSensorEntityDescription(
        name="DHW temperature (TW)",
        key="508",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "509": AmberModbusSensorEntityDescription(
        name="Heating/Cooling watertemperature (TC)",
        key="509",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "510": AmberModbusSensorEntityDescription(
        name="Heating/Cooling zone 1 watertemperature (TV1)",
        key="510",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "511": AmberModbusSensorEntityDescription(
        name="Heating/Cooling zone 2 watertemperature (TV2)",
        key="511",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
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
        suggested_display_precision=0,
        native_min_value=0,
        native_max_value=90,
        entity_registry_enabled_default=True,
    ),
    "516": AmberModbusSensorEntityDescription(
        name="EEV opening",
        key="516",
        icon="mdi:sine-wave",
    ),
    "517": AmberModbusSensorEntityDescription(
        name="Ambient temperature (TA)",
        key="517",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "518": AmberModbusSensorEntityDescription(
        name="1h Average ambient temperature",
        key="518",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "519": AmberModbusSensorEntityDescription(
        name="4h Average ambient temperature",
        key="519",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "520": AmberModbusSensorEntityDescription(
        name="24h Average ambient temperature",
        key="520",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "521": AmberModbusSensorEntityDescription(
        name="Compressor high pressure",
        key="521",
        native_unit_of_measurement = UnitOfPressure.BAR,
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "522": AmberModbusSensorEntityDescription(
        name="Compressor low pressure",
        key="522",
        native_unit_of_measurement = UnitOfPressure.BAR,
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "523": AmberModbusSensorEntityDescription(
        name="Compressor discharge temperature (Td)",
        key="523",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "524": AmberModbusSensorEntityDescription(
        name="Compressor suction temperature (Ts)",
        key="524",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "525": AmberModbusSensorEntityDescription(
        name="Coil temperature (TP)",
        key="525",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
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
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "529": AmberModbusSensorEntityDescription(
        name="Supply Voltage",
        key="529",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "530": AmberModbusSensorEntityDescription(
        name="Defrost status",
        key="530",
        icon="mdi:snowflake",
        entity_registry_enabled_default=True,
    ),    
    "531": AmberModbusSensorEntityDescription(
        name="Room temperature (TR)",
        key="531",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
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
        suggested_display_precision=0,
        entity_registry_enabled_default=True,
    ),
    "538": AmberModbusSensorEntityDescription(
        name="Mixing valve 1 ouputsignal",
        key="538",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "539": AmberModbusSensorEntityDescription(
        name="Mixing valve 2 ouputsignal",
        key="539",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "P01": AmberModbusSensorEntityDescription(
        name="P01 main line current protection",
        key="P01",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "P02": AmberModbusSensorEntityDescription(
        name="P02 compressor phase current protection",
        key="P02",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "P03": AmberModbusSensorEntityDescription(
        name="P03 ipm module protection",
        key="P03",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "P04": AmberModbusSensorEntityDescription(
        name="P04 compresor oil return protection",
        key="P04",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "P05": AmberModbusSensorEntityDescription(
        name="P05 high pressure refrigerant circuit",
        key="P05",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "P06": AmberModbusSensorEntityDescription(
        name="P06 very high pressure refrigerant circuit",
        key="P06",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "P07": AmberModbusSensorEntityDescription(
        name="P07 pre heat compressor",
        key="P07",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "P08": AmberModbusSensorEntityDescription(
        name="P08 gas discharge temp sensor protection",
        key="P08",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "P09": AmberModbusSensorEntityDescription(
        name="P09 evaporator coil temp sensor protection",
        key="P09",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "P10": AmberModbusSensorEntityDescription(
        name="P10 main voltage protection",
        key="P10",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ), 
    "P11": AmberModbusSensorEntityDescription(
        name="P11 compressor stop ambient temperature",
        key="P11",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "P12": AmberModbusSensorEntityDescription(
        name="P12 frequency limit compressor",
        key="P12",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "P13": AmberModbusSensorEntityDescription(
        name="P13 low pressure condensor pressure switch",
        key="P13",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F01": AmberModbusSensorEntityDescription(
        name="F01 failure ambient temperature sensor (Ta)",
        key="F01",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F02": AmberModbusSensorEntityDescription(
        name="F02 failure outdoor temperature sensor (Tp)",
        key="F02",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F03": AmberModbusSensorEntityDescription(
        name="F03 failure compressor discharge temperature sensor (Td)",
        key="F03",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F04": AmberModbusSensorEntityDescription(
        name="F04 failure compressor suction temperature sensor (Ts)",
        key="F04",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F05": AmberModbusSensorEntityDescription(
        name="F05 failure evporating pressure sensor (ps)",
        key="F05",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F06": AmberModbusSensorEntityDescription(
        name="F06 failure high pressure sensor (Pd)",
        key="F06",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F07": AmberModbusSensorEntityDescription(
        name="F07 failure high pressure switch",
        key="F07",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F09": AmberModbusSensorEntityDescription(
        name="F09 failure A fan motor",
        key="F09",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F10": AmberModbusSensorEntityDescription(
        name="F10 failure B fan motor",
        key="F10",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F11": AmberModbusSensorEntityDescription(
        name="F11 evporating pressure failure (Ps)",
        key="F11",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F12": AmberModbusSensorEntityDescription(
        name="F12 high pressure failure (Pd)",
        key="F12",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F13": AmberModbusSensorEntityDescription(
        name="F13 Room temperature sensor failure (Tr)",
        key="F13",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F14": AmberModbusSensorEntityDescription(
        name="F14 failure dhw tank temperature sensor (Tw)",
        key="F14",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F15": AmberModbusSensorEntityDescription(
        name="F15 Failure temperature control sensor (Tc)",
        key="F15",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F16": AmberModbusSensorEntityDescription(
        name="F16 failure outlet temperature sensor (Tuo)",
        key="F16",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F17": AmberModbusSensorEntityDescription(
        name="F17 failure inlet temperature sensor (Tui)",
        key="F17",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F18": AmberModbusSensorEntityDescription(
        name="F18 failure coil temperature sensor",
        key="F18",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F21": AmberModbusSensorEntityDescription(
        name="F21 failure water temperature sensor zone1 (Tv1)",
        key="F21",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F22": AmberModbusSensorEntityDescription(
        name="F22 failure water temperature sensor zone2 (Tv2)",
        key="F22",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F25": AmberModbusSensorEntityDescription(
        name="F25 communication failure",
        key="F25",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F27": AmberModbusSensorEntityDescription(
        name="F27 failure eeprom indoor unit",
        key="F27",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F28": AmberModbusSensorEntityDescription(
        name="F28 pwm signal failure pomp p0",
        key="F28",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F29": AmberModbusSensorEntityDescription(
        name="F29 failure 3-way valve zone1",
        key="F29",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "F30": AmberModbusSensorEntityDescription(
        name="F30 failure 3-way valve zone2",
        key="F30",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "E01": AmberModbusSensorEntityDescription(
        name="E01 comm failure lcd indoorunit",
        key="E01",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "E02": AmberModbusSensorEntityDescription(
        name="E02 failure outdoor_pcb_compressor_inverter",
        key="E02",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "E03": AmberModbusSensorEntityDescription(
        name="E03 power failure compressor",
        key="E03",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "E04": AmberModbusSensorEntityDescription(
        name="E04 overcurrent protection compressor",
        key="E04",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "E05": AmberModbusSensorEntityDescription(
        name="E05 compressor driver failure",
        key="E05",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "E06": AmberModbusSensorEntityDescription(
        name="E06 vdc unit failure",
        key="E06",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "E07": AmberModbusSensorEntityDescription(
        name="E07 ac current failure",
        key="E07",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "E08": AmberModbusSensorEntityDescription(
        name="E08 eeprom failure oudoor unit",
        key="E08",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "S01": AmberModbusSensorEntityDescription(
        name="S01 cooling anti freezing protection",
        key="S01",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "S02": AmberModbusSensorEntityDescription(
        name="S02 low flow warning",
        key="S02",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "S03": AmberModbusSensorEntityDescription(
        name="S03 flow switch failure",
        key="S03",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "S04": AmberModbusSensorEntityDescription(
        name="S04 communication failure indoor unit",
        key="S04",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "S05": AmberModbusSensorEntityDescription(
        name="S05 communication failure outdoor unit",
        key="S05",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "S06": AmberModbusSensorEntityDescription(
        name="S06 water outlet to low in cooling",
        key="S06",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "S07": AmberModbusSensorEntityDescription(
        name="S07 water outlet to high in heating",
        key="S07",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "S08": AmberModbusSensorEntityDescription(
        name="S08 defrost failure",
        key="S08",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "S09": AmberModbusSensorEntityDescription(
        name="S09 water outlet temperature low during defrost",
        key="S09",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "S10": AmberModbusSensorEntityDescription(
        name="S10 flow switch failure",
        key="S10",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "S11": AmberModbusSensorEntityDescription(
        name="S11 cooling anti freezing protection",
        key="S11",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "S13": AmberModbusSensorEntityDescription(
        name="S13 failure 4-way valve",
        key="S13",
        icon="mdi:alert",
        entity_registry_enabled_default=True,
    ),
    "703": AmberModbusSensorEntityDescription(
        name="Actual setpoint heating zone 1 ",
        key="703",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "704": AmberModbusSensorEntityDescription(
        name="Actual setpoint heating zone 2 ",
        key="704",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "714": AmberModbusSensorEntityDescription(
        name="Actual setpoint cooling zone 1 ",
        key="714",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "715": AmberModbusSensorEntityDescription(
        name="Actual setpoint cooling zone 2 ",
        key="715",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=True,
    ),
    "delta-T": AmberModbusSensorEntityDescription( 
        name="ΔT (Delta T) water outlet (Tuo) - water inlet (Tui)",
        key="delta-T",
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.KELVIN,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
    ),
    "connection_status": AmberModbusSensorEntityDescription(
        name="Connection Status",
        key="connection_status",
        icon="mdi:lan-connect",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=True,
    ),
}

@dataclass
class AmberModbusNumberEntityDescription(NumberEntityDescription):
    """Amber number entities."""

NUMBER_TYPES: dict[str, list[AmberModbusNumberEntityDescription]] = {
    # Writeble sensor values (numbers)
    "10": AmberModbusNumberEntityDescription(
        name="outside temperature start heating",
        key= "10",
        mode="slider",
        native_min_value= -10,
        native_max_value= 25, 
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "11": AmberModbusNumberEntityDescription(
        name="outside temperature start cooling",
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
    "31":AmberModbusNumberEntityDescription(
        name="Heatcurve outside temperature 1",
        key="31",
        mode="slider",
        native_min_value= -25,
        native_max_value= 25,
        icon="mdi:thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "32":AmberModbusNumberEntityDescription(
        name="Heatcurve outside temperature 2",
        key="32",
        mode="slider",
        native_min_value= -25,
        native_max_value= 25,
        icon="mdi:thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "33":AmberModbusNumberEntityDescription(
        name="Heatcurve outside temperature 3",
        key="33",
        mode="slider",
        native_min_value= -25,
        native_max_value= 25,
        icon="mdi:thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "34":AmberModbusNumberEntityDescription(
        name="Heatcurve outside temperature 4",
        key="34",
        mode="slider",
        native_min_value= -25,
        native_max_value= 25,
        icon="mdi:thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "35":AmberModbusNumberEntityDescription(
        name="Heatcurve outside temperature 5",
        key="35",
        mode="slider",
        native_min_value= -25,
        native_max_value= 25,
        icon="mdi:thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "36":AmberModbusNumberEntityDescription(
        name="Heatcurve-1 setpoint-1",
        key="36",
        mode="slider",
        native_min_value= 20,
        native_max_value= 45,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "37":AmberModbusNumberEntityDescription(
        name="Heatcurve-1 setpoint-2",
        key="37",
        mode="slider",
        native_min_value= 20,
        native_max_value= 45,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "38":AmberModbusNumberEntityDescription(
        name="Heatcurve-1 setpoint-3",
        key="38",
        mode="slider",
        native_min_value= 20,
        native_max_value= 45,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "39":AmberModbusNumberEntityDescription(
        name="Heatcurve-1 setpoint-4",
        key="39",
        mode="slider",
        native_min_value= 20,
        native_max_value= 45,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "40":AmberModbusNumberEntityDescription(
        name="Heatcurve-1 setpoint-5",
        key="40",
        mode="slider",
        native_min_value= 20,
        native_max_value= 45,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "42":AmberModbusNumberEntityDescription(
        name="Ideal room temperature in heating",
        key="42",
        mode="slider",
        native_min_value= 15,
        native_max_value= 35,
        icon="mdi:thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "43":AmberModbusNumberEntityDescription(
        name="Ideal room temperature in cooling",
        key="43",
        mode="slider",
        native_min_value= 15,
        native_max_value= 35,
        icon="mdi:thermometer-outline",
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
        name="room temperature vacation mode",
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
    "93": AmberModbusNumberEntityDescription(
        name="Heatcurve-2 setpoint-1",
        key="93",
        mode="slider",
        native_min_value= 20,
        native_max_value= 45,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "94": AmberModbusNumberEntityDescription(
        name="Heatcurve-2 setpoint-2",
        key="94",
        mode="slider",
        native_min_value= 20,
        native_max_value= 45,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "95": AmberModbusNumberEntityDescription(
        name="Heatcurve-2 setpoint-3",
        key="95",
        mode="slider",
        native_min_value= 20,
        native_max_value= 45,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "96": AmberModbusNumberEntityDescription(
        name="Heatcurve-2 setpoint-4",
        key="96",
        mode="slider",
        native_min_value= 20,
        native_max_value= 45,
        icon="mdi:water-thermometer-outline",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "97": AmberModbusNumberEntityDescription(
        name="Heatcurve-2 setpoint-5",
        key="97",
        mode="slider",
        native_min_value= 20,
        native_max_value= 45,
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
        name="outsidetemperature start dhw eco mode",
        key="133",
        mode="slider",
        native_min_value= -20,
        native_max_value= 43,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=True,
    ),
    "134": AmberModbusNumberEntityDescription(
        name="outside temperature start external heating",
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
        #
        name="temperature zone 2",
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