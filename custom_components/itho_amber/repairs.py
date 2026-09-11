import logging
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry

_LOGGER = logging.getLogger(__name__)

MIGRATIONS = {
    #Realtime sensors
    "sensor.amber_room_temperture_tr": {
        "new_entity_id": "sensor.amber_room_temperature_tr",
        "new_name": "Room temperature (TR)",
    },
    "sensor.amber_condenser_temperture_tup":{
        "new_entity_id": "sensor.amber_condenser_temperature_tup",
        "new_name": "Condenser temperature (TUP)",
    },
    "sensor.amber_dhw_temperture_tw":{
        "new_entity_id": "sensor.amber_dhw_temperature_tw",
        "new_name": "DHW temperature (TW)",
    },
    "sensor.amber_heating_cooling_watertemperture_tc":{
        "new_entity_id": "sensor.amber_heating_cooling_water_temperature_tc",
        "new_name": "Heating/Cooling watertemperature (TC)",
    },
    "sensor.amber_heating_cooling_zone_1_watertemperture_tv1":{
        "new_entity_id": "sensor.amber_heating_cooling_zone_1_water_temperature_tv1",
        "new_name": "Heating/Cooling zone 1 watertemperature (TV1)",
    },
    "sensor.amber_heating_cooling_zone_2_watertemperture_tv2":{
        "new_entity_id": "sensor.amber_heating_cooling_zone_2_water_temperature_tv2",
        "new_name": "Heating/Cooling zone 2 watertemperature (TV2)",
    },
    "sensor.amber_ambient_temperture_ta":{
        "new_entity_id": "sensor.amber_ambient_temperature_ta",
        "new_name": "Ambient temperature (TA)"
    },
    "sensor.amber_1h_average_ambient_temperture":{
        "new_entity_id": "sensor.amber_1h_average_ambient_temperature",
        "new_name": "1h Average ambient temperature"
    },
    "sensor.amber_4h_average_ambient_temperture":{
        "new_entity_id": "sensor.amber_4h_average_ambient_temperature",
        "new_name": "4h Average ambient temperature"
    },
    "sensor.amber_24h_average_ambient_temperture":{
        "new_entity_id": "sensor.amber_24h_average_ambient_temperature",
        "new_name": "24h Average ambient temperature"
    },
    "sensor.amber_compressor_discharge_temperture":{
        "new_entity_id": "sensor.amber_compressor_discharge_temperature",
        "new_name": "Compressor discharge temperature (Td)"
    },
    "sensor.amber_compressor_suction_temperture":{
        "new_entity_id": "sensor.amber_compressor_suction_temperature",
        "new_name": "Compressor suction temperature (Ts)"
    },
    "sensor.amber_coil_temperture_tp":{
        "new_entity_id": "sensor.amber_coil_temperature_tp",
        "new_name": "Coil temperature (TP)"
    },
    #Fault codes
    "sensor.amber_p11_compressor_stop_ambient_temperture":{
        "new_entity_id": "sensor.amber_p11_compressor_stop_ambient_temperature",
        "new_name": "P11 compressor stop ambient temperature"
    },
    "sensor.amber_f01_failure_ambient_temperture_sensor_ta":{
        "new_entity_id": "sensor.amber_f01_failure_ambient_temperature_sensor_ta",
        "new_name": "F01 failure ambient temperature sensor (Ta)"
    },
    "sensor.amber_f02_failure_outdoor_temperture_sensor_tp":{
        "new_entity_id": "sensor.amber_f02_failure_outdoor_temperature_sensor_tp",
        "new_name": "F02 failure outdoor temperature sensor (Tp)"
    },
    "sensor.amber_f03_failure_compressor_discharge_temperture_sensor_tp":{
        "new_entity_id": "sensor.amber_f03_failure_compressor_discharge_temperature_sensor_td",
        "new_name": "F03 failure compressor discharge temperature sensor (Td)"
    },
    "sensor.amber_f04_failure_compressor_suction_temperture_sensor_ts":{
        "new_entity_id": "sensor.amber_f04_failure_compressor_suction_temperature_sensor_ts",
        "new_name": "F04 failure compressor suction temperature sensor (Ts)"
    },
    "sensor.amber_f13_room_temp_sensor_failure_tr":{
        "new_entity_id": "sensor.amber_f13_room_temperature_sensor_failure_tr",
        "new_name": "F13 Room temperature sensor failure (Tr)"
    },
    "sensor.amber_f14_failure_dhw_tank_sensor_tw":{
        "new_entity_id": "sensor.amber_f14_failure_dhw_tank_temperature_sensor_tw",
        "new_name": "F14 failure dhw tank temperature sensor (Tw)"
    },
    "sensor.amber_f15_failure_temperture_control_sensor_tc":{
        "new_entity_id": "sensor.amber_f15_failure_temperature_control_sensor_tc",
        "new_name": "F15 Failure temperature control sensor (Tc)"
    },
    "sensor.amber_f16_failure_outlet_temperture_sensor_tuo":{
        "new_entity_id": "sensor.amber_f16_failure_outlet_temperature_sensor_tuo",
        "new_name": "F16 failure outlet temperature sensor (Tuo)"
    },
    "sensor.amber_f17_failure_inlet_temperture_sensor_tui":{
        "new_entity_id": "sensor.amber_f17_failure_inlet_temperature_sensor_tui",
        "new_name": "F17 failure inlet temperature sensor (Tui)"
    },
    "sensor.amber_f18_failure_coil_temperture_sensor":{
        "new_entity_id": "sensor.amber_f18_failure_coil_temperature_sensor",
        "new_name": "F18 failure coil temperature sensor"
    },
    "sensor.amber_f21_failure_water_temperture_sensor_zone1_tv1":{
        "new_entity_id": "sensor.amber_f21_failure_water_temperature_sensor_zone1_tv1",
        "new_name": "F21 failure water temperature sensor zone1 (Tv1)"
    },
    "sensor.amber_f22_failure_water_temperture_sensor_zone2_tv2":{
        "new_entity_id": "sensor.amber_f22_failure_water_temperature_sensor_zone2_tv2",
        "new_name": "F22 failure water temperature sensor zone2 (Tv2)"
    },
    "sensor.amber_s09_water_outlet_temp_low_during_defrost":{
        "new_entity_id": "sensor.amber_s09_water_outlet_temperature_low_during_defrost",
        "new_name": "S09 water outlet temperature low during defrost"
    },
    #settings
    "sensor.amber_room_temperture_sensor":{
        "new_entity_id": "sensor.amber_room_temperature_sensor",
        "new_name": "room temperature sensor"
    },
    "sensor.amber_temperture_rise_interval_hwtbh":{
        "new_entity_id": "sensor.amber_temperature_rise_interval_hwtbh",
        "new_name": "temperature rise interval hwtbh"
    },
    "sensor.amber_shifting_priority_dhw_temperture":{
        "new_entity_id": "sensor.amber_shifting_priority_dhw_temperature",
        "new_name": "shifting priority dhw temperature"
    },
    "sensor.amber_shifting_priority_temperture_diff":{
        "new_entity_id": "sensor.amber_shifting_priority_temperature_diff",
        "new_name": "shifting priority temperature diff"
    },
    "sensor.amber_min_temperture_timer_dhw":{
        "new_entity_id": "sensor.amber_min_temperature_timer_dhw",
        "new_name": "min temperature timer dhw"
    },
    "sensor.amber_min_temperture_setpoint_dhw":{
        "new_entity_id": "sensor.amber_min_temperature_setpoint_dhw",
        "new_name": "min temperature setpoint dhw"
    },
    "sensor.amber_restart_min_temperture_dhw":{
        "new_entity_id": "sensor.amber_restart_min_temperature_dhw",
        "new_name": "restart min temperature dhw"
    },
    "sensor.amber_outside_start_temperture_frost_protection_first_stage":{
        "new_entity_id": "sensor.amber_outside_start_temperature_frost_protection_first_stage",
        "new_name": "outside start temperature frost protection first stage"
    },
    "sensor.amber_outside_start_temperture_frost_protection_second_stage":{
        "new_entity_id": "sensor.amber_outside_start_temperature_frost_protection_second_stage",
        "new_name": "outside start temperature frost protection second stage"
    },
    "sensor.amber_outside_stop_temperture_frost_protection_first_stage":{
        "new_entity_id": "sensor.amber_outside_stop_temperature_frost_protection_first_stage",
        "new_name": "outside stop temperature frost protection first stage"
    },
    "sensor.amber_water_start_temperture_frost_protection_second_stage":{
        "new_entity_id": "sensor.amber_water_start_temperature_frost_protection_second_stage",
        "new_name": "water start temperature frost protection second stage"
    },
    "sensor.amber_water_stop_temperture_frost_protection_second_stage":{
        "new_entity_id": "sensor.amber_water_stop_temperature_frost_protection_second_stage",
        "new_name": "water stop temperature frost protection second stage"
    },
    "sensor.amber_block_external_heating_on_outsidetemperture":{
        "new_entity_id": "sensor.amber_block_external_heating_on_outside_temperature",
        "new_name": "block external heating on outsidetemperature"
    },
    "sensor.amber_setpoint_block_external_heating_on_outsidetemperture":{
        "new_entity_id": "sensor.amber_setpoint_block_external_heating_on_outside_temperature",
        "new_name": "setpoint block external heating on outsidetemperature"
    },
    "sensor.amber_coolcurve_outside_temperture_1":{
        "new_entity_id": "sensor.amber_coolcurve_outside_temperature_1",
        "new_name": "coolcurve outside temperature 1"
    },
    "sensor.amber_coolcurve_outside_temperture_2":{
        "new_entity_id": "sensor.amber_coolcurve_outside_temperature_2",
        "new_name": "coolcurve outside temperature 2"
    },
    "sensor.amber_coolcurve_outside_temperture_3":{
        "new_entity_id": "sensor.amber_coolcurve_outside_temperature_3",
        "new_name": "coolcurve outside temperature 3"
    },
    "number.amber_outside_temperture_start_heating":{
        "new_entity_id": "number.amber_outside_temperature_start_heating",
        "new_name": "outside temperature start heating"
    },
    "number.amber_outside_temperture_start_cooling":{
        "new_entity_id": "number.amber_outside_temperature_start_cooling",
        "new_name": "outside temperature start cooling"
    },
    "number.amber_heatcurve_outside_temperture_1":{
        "new_entity_id": "number.amber_heatcurve_outside_temperature_1",
        "new_name": "heatcurve outside temperature 1"
    },
    "number.amber_heatcurve_outside_temperture_2":{
        "new_entity_id": "number.amber_heatcurve_outside_temperature_2",
        "new_name": "heatcurve outside temperature 2"
    },
    "number.amber_heatcurve_outside_temperture_3":{
        "new_entity_id": "number.amber_heatcurve_outside_temperature_3",
        "new_name": "heatcurve outside temperature 3"
    },
    "number.amber_heatcurve_outside_temperture_4":{
        "new_entity_id": "number.amber_heatcurve_outside_temperature_4",
        "new_name": "heatcurve outside temperature 4"
    },
    "number.amber_heatcurve_outside_temperture_5":{
        "new_entity_id": "number.amber_heatcurve_outside_temperature_5",
        "new_name": "heatcurve outside temperature 5"
    },
    "number.amber_ideal_room_temp_inheating":{
        "new_entity_id": "number.amber_ideal_room_temperature_in_heating",
        "new_name": "ideal room temperature in heating"
    },
    "number.amber_ideal_room_temp_incooling":{
        "new_entity_id": "number.amber_ideal_room_temperature_in_cooling",
        "new_name": "ideal room temperature in cooling"
    },
    "number.amber_room_temperture_vacation_mode":{
        "new_entity_id": "number.amber_room_temperature_vacation_mode",
        "new_name": "room temperature vacation mode"
    },
    "number.amber_outside_temperture_start_external_heating":{
        "new_entity_id": "number.amber_outside_temperature_start_external_heating",
        "new_name": "outside temperature start external heating"
    },
    "number.amber_outsidetemperture_start_dhw_eco_mode":{
        "new_entity_id": "number.amber_outside_temperature_start_dhw_eco_mode",
        "new_name": "outside temperature start dhw eco mode"
    },
    #switch
    "switch.amber_temperture_zone_2":{
        "new_entity_id": "switch.amber_temperature_zone_2",
        "new_name": "temperature zone 2"
    },
    # 1.4.0-beta3: spelling / spacing fixes in entity names
    "sensor.amber_heating_cooling_watertemperature_tc": {
        "new_entity_id": "sensor.amber_heating_cooling_water_temperature_tc",
        "new_name": "Heating/Cooling water temperature (TC)",
    },
    "sensor.amber_heating_cooling_zone_1_watertemperature_tv1": {
        "new_entity_id": "sensor.amber_heating_cooling_zone_1_water_temperature_tv1",
        "new_name": "Heating/Cooling zone 1 water temperature (TV1)",
    },
    "sensor.amber_heating_cooling_zone_2_watertemperature_tv2": {
        "new_entity_id": "sensor.amber_heating_cooling_zone_2_water_temperature_tv2",
        "new_name": "Heating/Cooling zone 2 water temperature (TV2)",
    },
    "sensor.amber_block_external_heating_on_outsidetemperature": {
        "new_entity_id": "sensor.amber_block_external_heating_on_outside_temperature",
        "new_name": "Block external heating on outside temperature",
    },
    "sensor.amber_setpoint_block_external_heating_on_outsidetemperature": {
        "new_entity_id": "sensor.amber_setpoint_block_external_heating_on_outside_temperature",
        "new_name": "Setpoint block external heating on outside temperature",
    },
    "number.amber_outsidetemperature_start_dhw_eco_mode": {
        "new_entity_id": "number.amber_outside_temperature_start_dhw_eco_mode",
        "new_name": "Outside temperature start dhw eco mode",
    },
    "sensor.amber_sg_decrease_setrpoint_cooling": {
        "new_entity_id": "sensor.amber_sg_decrease_setpoint_cooling",
        "new_name": "SG decrease setpoint cooling",
    },
    "sensor.amber_mixing_valve_1_ouputsignal": {
        "new_entity_id": "sensor.amber_mixing_valve_1_output_signal",
        "new_name": "Mixing valve 1 output signal",
    },
    "sensor.amber_mixing_valve_2_ouputsignal": {
        "new_entity_id": "sensor.amber_mixing_valve_2_output_signal",
        "new_name": "Mixing valve 2 output signal",
    },
    "sensor.amber_p04_compresor_oil_return_protection": {
        "new_entity_id": "sensor.amber_p04_compressor_oil_return_protection",
        "new_name": "P04 compressor oil return protection",
    },
    "sensor.amber_p13_low_pressure_condensor_pressure_switch": {
        "new_entity_id": "sensor.amber_p13_low_pressure_condenser_pressure_switch",
        "new_name": "P13 low pressure condenser pressure switch",
    },
    "sensor.amber_f05_failure_evporating_pressure_sensor_ps": {
        "new_entity_id": "sensor.amber_f05_failure_evaporating_pressure_sensor_ps",
        "new_name": "F05 failure evaporating pressure sensor (ps)",
    },
    "sensor.amber_f11_evporating_pressure_failure_ps": {
        "new_entity_id": "sensor.amber_f11_evaporating_pressure_failure_ps",
        "new_name": "F11 evaporating pressure failure (Ps)",
    },
    "sensor.amber_e01_comm_failure_lcd_indoorunit": {
        "new_entity_id": "sensor.amber_e01_comm_failure_lcd_indoor_unit",
        "new_name": "E01 comm failure lcd indoor unit",
    },
    "sensor.amber_e08_eeprom_failure_oudoor_unit": {
        "new_entity_id": "sensor.amber_e08_eeprom_failure_outdoor_unit",
        "new_name": "E08 eeprom failure outdoor unit",
    },
    # The entity name says (Td) but the earlier migration and the alarm
    # monitor used _tp, so a fresh install was never monitored for F03.
    "sensor.amber_f03_failure_compressor_discharge_temperature_sensor_tp": {
        "new_entity_id": "sensor.amber_f03_failure_compressor_discharge_temperature_sensor_td",
        "new_name": "F03 failure compressor discharge temperature sensor (Td)",
    },
}

# Names an earlier version of this migration wrote into the entity registry
# as a user override. Only these are ever cleared again - a name the user
# chose themselves is left alone.
_MIGRATION_NAMES = {data["new_name"] for data in MIGRATIONS.values()}


async def async_migrate_temperature_typo(hass):
    er = async_get_entity_registry(hass)
    changed = False

    for old_entity_id, data in MIGRATIONS.items():
        entity = er.entities.get(old_entity_id)
        if entity is None:
            continue
        if er.async_get(data["new_entity_id"]) is not None:
            _LOGGER.warning(
                "Migration: cannot rename %s, %s already exists",
                old_entity_id,
                data["new_entity_id"],
            )
            continue

        _LOGGER.warning(
            "Migration: renaming %s -> %s", old_entity_id, data["new_entity_id"]
        )
        kwargs = {"new_entity_id": data["new_entity_id"]}
        if entity.name in _MIGRATION_NAMES:
            kwargs["name"] = None
        er.async_update_entity(old_entity_id, **kwargs)
        changed = True

    # Installs migrated by an earlier version still carry the old lowercase
    # (sometimes misspelled) name as a registry override, which hides the
    # corrected name from const.py. Clear it.
    for data in MIGRATIONS.values():
        entity = er.entities.get(data["new_entity_id"])
        if entity is not None and entity.name in _MIGRATION_NAMES:
            _LOGGER.info("Migration: clearing name override on %s", data["new_entity_id"])
            er.async_update_entity(data["new_entity_id"], name=None)
            changed = True

    return changed