"""platform for select integration."""

from __future__ import annotations
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.select import SelectEntity

from homeassistant.const import CONF_NAME
from homeassistant.core import callback
import homeassistant.util.dt as dt_util

from pymodbus.client import ModbusTcpClient
#from pymodbus.payload import BinaryPayloadBuilder

from .const import (
    ATTR_MANUFACTURER,
    DOMAIN,
    SELECT_CONTROL,
    SELECT_WORKING,
    EXTERNAL_CONTROL,
    SELECT_HWTBH,
    SELECT_PUMP_P0_WORKING_MODE,
    PUMP_P0_WORKING_MODE,
    PUMP_SPEED,
    SELECT_PUMP_P0_SPEED,
    CURRENT_WORKING_MODE,
    HWTBH_PRIORITY_MODE,
    AmberModbusSelectEntityControlDescription,
    AmberModbusSelectEntityWorkingDescription,
    AmberModbusSelectEntityHWTBHPriorityDescription,
    AmberModbusSelectEntityP0PumpModeDescription,
    AmberModbusSelectEntityP0PumpSpeedDescription,
)

async def async_setup_entry(hass, entry, async_add_entities):
    hub_name = entry.data[CONF_NAME]
    hub = hass.data[DOMAIN][hub_name]["hub"]

    device_info = {
        "identifiers": {(DOMAIN, hub_name)},
        "name": hub_name,
        "manufacturer": ATTR_MANUFACTURER,
    }

    entities = []
    for select_description in SELECT_CONTROL.values():
        select = AmberSelectControlMode(
            hub_name,
            hub,
            device_info,
            select_description,
        )
        entities.append(select)

    for select_description in SELECT_WORKING.values():
        control = AmberSelectWorkingMode(
            hub_name,
            hub,
            device_info,
            select_description,
        )
        entities.append(control)

    for select_description in SELECT_HWTBH.values():
        control = AmberSelectHWTBHMode(
            hub_name,
            hub,
            device_info,
            select_description,
        )
        entities.append(control)

    for select_description in SELECT_PUMP_P0_WORKING_MODE.values():
        control = AmberSelectP0PumpMode(
            hub_name,
            hub,
            device_info,
            select_description,
        )
        entities.append(control)

    for select_description in SELECT_PUMP_P0_SPEED.values():
        control = AmberSelectP0PumpSpeed(
            hub_name,
            hub,
            device_info,
            select_description,
        )
        entities.append(control)

    async_add_entities(entities)
    return True

def get_key(d, search):
    for k, v in d.items():
        if v == search:
            return k
    return None

class AmberSelectControlMode(CoordinatorEntity, SelectEntity):
    """Representation of a Amber Modbus select.""" 

    def __init__(
        self,
        platform_name: str,
        hub: AmberModbusHub,
        device_info,
        description: AmberModbusSelectEntityControlDescription,
    ):
        """Initialize the select."""
        self._platform_name = platform_name
        self._attr_device_info = device_info
        self.entity_description: AmberModbusSelectEntityControlDescription = description
        self._hub = hub
        self._options = EXTERNAL_CONTROL
        self._attr_options = list(self._options.values())

        super().__init__(coordinator=hub)

    @property
    def name(self):
        """Return the name."""
        return f"{self._platform_name} {self.entity_description.name}"

    @property
    def unique_id(self) -> Optional[str]:
        return f"{self._platform_name}_{self.entity_description.key}"
    
    @property
    def current_option(self):
        value = self.coordinator.data[self.entity_description.key]
        if value in EXTERNAL_CONTROL:
            selected = EXTERNAL_CONTROL[value]
        return selected
    
    def select_option(self, option) -> None:
        address = int(self.entity_description.key)
        new_mode = get_key(self._options, option)
        self._hub.write_registers(address, payload=ModbusTcpClient.convert_to_registers(int(new_mode), data_type=ModbusTcpClient.DATATYPE.INT16, word_order="big"))

class AmberSelectWorkingMode(CoordinatorEntity, SelectEntity):
    """Representation of a Amber Modbus select."""

    def __init__(
        self,
        platform_name: str,
        hub: AmberModbusHub,
        device_info,
        description: AmberModbusSelectEntityWorkingDescription,
    ):
        """Initialize the select."""
        self._platform_name = platform_name
        self._attr_device_info = device_info
        self.entity_description: AmberModbusSelectEntityWorkingDescription = description
        self._hub = hub
        self._options = CURRENT_WORKING_MODE
        self._attr_options = list(self._options.values())

        super().__init__(coordinator=hub)

    @property
    def name(self):
        """Return the name."""
        return f"{self._platform_name} {self.entity_description.name}"

    @property
    def unique_id(self) -> Optional[str]:
        return f"{self._platform_name}_{self.entity_description.key}"
    
    @property
    def current_option(self):
        value = self.coordinator.data[self.entity_description.key]
        if value in CURRENT_WORKING_MODE:
            selected = CURRENT_WORKING_MODE[value]
        return selected
    
    def select_option(self, option) -> None:
        address = int(self.entity_description.key)
        new_mode = get_key(self._options, option)
        self._hub.write_registers(address, payload=ModbusTcpClient.convert_to_registers(int(new_mode), data_type=ModbusTcpClient.DATATYPE.INT16, word_order="big"))

class AmberSelectHWTBHMode(CoordinatorEntity, SelectEntity):
    """Representation of a Amber Modbus select."""

    def __init__(
        self,
        platform_name: str,
        hub: AmberModbusHub,
        device_info,
        description: AmberModbusSelectEntityHWTBHPriorityDescription,
    ):
        """Initialize the select."""
        self._platform_name = platform_name
        self._attr_device_info = device_info
        self.entity_description: AmberModbusSelectEntityHWTBHPriorityDescription = description
        self._hub = hub
        self._options = HWTBH_PRIORITY_MODE
        self._attr_options = list(self._options.values())

        super().__init__(coordinator=hub)

    @property
    def name(self):
        """Return the name."""
        return f"{self._platform_name} {self.entity_description.name}"

    @property
    def unique_id(self) -> Optional[str]:
        return f"{self._platform_name}_{self.entity_description.key}"
    
    @property
    def current_option(self):
        value = self.coordinator.data[self.entity_description.key]
        if value in HWTBH_PRIORITY_MODE:
            selected = HWTBH_PRIORITY_MODE[value]
        return selected
    
    def select_option(self, option) -> None:
        address = int(self.entity_description.key)
        new_mode = get_key(self._options, option)
        self._hub.write_registers(address, payload=ModbusTcpClient.convert_to_registers(int(new_mode), data_type=ModbusTcpClient.DATATYPE.INT16, word_order="big"))

class AmberSelectP0PumpMode(CoordinatorEntity, SelectEntity):
    """Representation of a Amber Modbus select."""

    def __init__(
        self,
        platform_name: str,
        hub: AmberModbusHub,
        device_info,
        description: AmberModbusSelectEntityP0PumpModeDescription,
    ):
        """Initialize the select."""
        self._platform_name = platform_name
        self._attr_device_info = device_info
        self.entity_description: AmberModbusSelectEntityP0PumpModeDescription = description
        self._hub = hub
        self._options = PUMP_P0_WORKING_MODE
        self._attr_options = list(self._options.values())

        super().__init__(coordinator=hub)

    @property
    def name(self):
        """Return the name."""
        return f"{self._platform_name} {self.entity_description.name}"

    @property
    def unique_id(self) -> Optional[str]:
        return f"{self._platform_name}_{self.entity_description.key}"
    
    @property
    def current_option(self):
        value = self.coordinator.data[self.entity_description.key]
        if value in PUMP_P0_WORKING_MODE:
            selected = PUMP_P0_WORKING_MODE[value]
        return selected
    
    def select_option(self, option) -> None:
        address = int(self.entity_description.key)
        new_mode = get_key(self._options, option)
        self._hub.write_registers(address, payload=ModbusTcpClient.convert_to_registers(int(new_mode), data_type=ModbusTcpClient.DATATYPE.INT16, word_order="big"))

class AmberSelectP0PumpSpeed(CoordinatorEntity, SelectEntity):
    """Representation of a Amber Modbus Pump 0 speed select."""

    def __init__(
        self,
        platform_name: str,
        hub: AmberModbusHub,
        device_info,
        description: AmberModbusSelectEntityP0PumpSpeedDescription,
    ):
        """Initialize the select."""
        self._platform_name = platform_name
        self._attr_device_info = device_info
        self.entity_description: AmberModbusSelectEntityP0PumpSpeedDescription = description
        self._hub = hub
        self._options = PUMP_SPEED
        self._attr_options = list(self._options.values())

        super().__init__(coordinator=hub)

    @property
    def name(self):
        """Return the name."""
        return f"{self._platform_name} {self.entity_description.name}"

    @property
    def unique_id(self) -> Optional[str]:
        return f"{self._platform_name}_{self.entity_description.key}"
    
    @property
    def current_option(self):
        value = self.coordinator.data[self.entity_description.key]
        if value in PUMP_SPEED:
            selected = PUMP_SPEED[value]
        return selected
    
    def select_option(self, option) -> None:
        address = int(self.entity_description.key)
        new_mode = get_key(self._options, option)
        self._hub.write_registers(address, payload=ModbusTcpClient.convert_to_registers(int(new_mode), data_type=ModbusTcpClient.DATATYPE.INT16, word_order="big"))