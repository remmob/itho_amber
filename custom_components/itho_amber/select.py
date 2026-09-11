"""platform for select integration."""

from __future__ import annotations
import asyncio
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.select import SelectEntity

from homeassistant.const import CONF_NAME
from homeassistant.core import callback
import homeassistant.util.dt as dt_util

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
    DEFAULT_NAME,
    ATTR_COPYRIGHT,
    ATTR_SW_VERSION,
)

async def async_setup_entry(hass, entry, async_add_entities):
    hub_name = entry.data[CONF_NAME]
    hub = hass.data[DOMAIN][hub_name]["hub"]

    device_info = {
        "identifiers": {(DOMAIN, hub_name)},
        "name": DEFAULT_NAME,
        "model": ATTR_MANUFACTURER,
        "manufacturer": ATTR_COPYRIGHT,
        "sw_version": ATTR_SW_VERSION,
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

# After writing, wait for the coordinator's next read(s) to confirm the new
# value before returning - Home Assistant writes entity state right after
# select_option() returns, so returning early (before the write has been
# read back) shows the old option for one refresh cycle before flipping to
# the new one. Same fix already applied to switch.py's turn_on/turn_off.
POLL_FREQUENCY_SECONDS = 15
MAX_STATUS_CHANGE_TIME_SECONDS = 30

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
        """Return the currently selected option."""
        value = self.coordinator.data.get(self.entity_description.key)

        selected = None 

        if value in EXTERNAL_CONTROL:
            selected = EXTERNAL_CONTROL[value]
        else:
            if self._attr_options:
                selected = self._attr_options[0]

        return selected

    # @property
    # def current_option(self):
    #     value = self.coordinator.data[self.entity_description.key]
    #     if value in EXTERNAL_CONTROL:
    #         selected = EXTERNAL_CONTROL[value]
    #     return selected
    
    async def async_select_option(self, option: str) -> None:
        """Send the new option and wait for it to be confirmed by the next read."""
        address = int(self.entity_description.key)
        new_mode = get_key(self._options, option)
        self._hub.write_registers(address, int(new_mode))

        for _ in range(MAX_STATUS_CHANGE_TIME_SECONDS // POLL_FREQUENCY_SECONDS):
            await asyncio.sleep(POLL_FREQUENCY_SECONDS)
            if self.coordinator.data.get(self.entity_description.key) == new_mode:
                break

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
        """Return the currently selected option."""
        value = self.coordinator.data.get(self.entity_description.key)

        selected = None

        if value in CURRENT_WORKING_MODE:
            selected = CURRENT_WORKING_MODE[value]
        else:
            if self._attr_options:
                selected = self._attr_options[0]

        return selected

    # @property
    # def current_option(self):
    #     value = self.coordinator.data[self.entity_description.key]
    #     if value in CURRENT_WORKING_MODE:
    #         selected = CURRENT_WORKING_MODE[value]
    #     return selected
    
    async def async_select_option(self, option: str) -> None:
        """Send the new option and wait for it to be confirmed by the next read."""
        address = int(self.entity_description.key)
        new_mode = get_key(self._options, option)
        self._hub.write_registers(address, int(new_mode))

        for _ in range(MAX_STATUS_CHANGE_TIME_SECONDS // POLL_FREQUENCY_SECONDS):
            await asyncio.sleep(POLL_FREQUENCY_SECONDS)
            if self.coordinator.data.get(self.entity_description.key) == new_mode:
                break

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
        """Return the currently selected option."""
        value = self.coordinator.data.get(self.entity_description.key)

        selected = None

        if value in HWTBH_PRIORITY_MODE:
            selected = HWTBH_PRIORITY_MODE[value]
        else:
            if self._attr_options:
                selected = self._attr_options[0]

        return selected

    # @property
    # def current_option(self):
    #     value = self.coordinator.data[self.entity_description.key]
    #     if value in HWTBH_PRIORITY_MODE:
    #         selected = HWTBH_PRIORITY_MODE[value]
    #     return selected
    
    async def async_select_option(self, option: str) -> None:
        """Send the new option and wait for it to be confirmed by the next read."""
        address = int(self.entity_description.key)
        new_mode = get_key(self._options, option)
        self._hub.write_registers(address, int(new_mode))

        for _ in range(MAX_STATUS_CHANGE_TIME_SECONDS // POLL_FREQUENCY_SECONDS):
            await asyncio.sleep(POLL_FREQUENCY_SECONDS)
            if self.coordinator.data.get(self.entity_description.key) == new_mode:
                break

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
        """Return the currently selected option."""
        value = self.coordinator.data.get(self.entity_description.key)

        selected = None

        if value in PUMP_P0_WORKING_MODE:
            selected = PUMP_P0_WORKING_MODE[value]
        else:
            if self._attr_options:
                selected = self._attr_options[0]

        return selected

    
    # @property
    # def current_option(self):
    #     value = self.coordinator.data[self.entity_description.key]
    #     if value in PUMP_P0_WORKING_MODE:
    #         selected = PUMP_P0_WORKING_MODE[value]
    #     return selected
    
    async def async_select_option(self, option: str) -> None:
        """Send the new option and wait for it to be confirmed by the next read."""
        address = int(self.entity_description.key)
        new_mode = get_key(self._options, option)
        self._hub.write_registers(address, int(new_mode))

        for _ in range(MAX_STATUS_CHANGE_TIME_SECONDS // POLL_FREQUENCY_SECONDS):
            await asyncio.sleep(POLL_FREQUENCY_SECONDS)
            if self.coordinator.data.get(self.entity_description.key) == new_mode:
                break

class AmberSelectP0PumpSpeed(CoordinatorEntity, SelectEntity):
    def __init__(self, platform_name, hub, device_info, description):
        self._platform_name = platform_name
        self._attr_device_info = device_info
        self.entity_description = description
        self._hub = hub
        self._options = PUMP_SPEED
        self._attr_options = list(self._options.values())
        super().__init__(coordinator=hub)

    @property
    def name(self):
        return f"{self._platform_name} {self.entity_description.name}"

    @property
    def unique_id(self) -> Optional[str]:
        return f"{self._platform_name}_{self.entity_description.key}"

    @property
    def current_option(self):
        """Return the currently selected option."""
        value = self.coordinator.data.get(self.entity_description.key)

        selected = None

        if value in PUMP_SPEED:
            selected = PUMP_SPEED[value]
        else:
            if self._attr_options:
                selected = self._attr_options[0]

        return selected

    
    # @property
    # def current_option(self):
    #     value = self.coordinator.data.get(self.entity_description.key)
    #     return PUMP_SPEED.get(value)
   
    async def async_select_option(self, option: str) -> None:
        """Send the new option and wait for it to be confirmed by the next read."""
        address = int(self.entity_description.key)
        new_mode = get_key(self._options, option)

        self._hub.write_registers(address, int(new_mode))

        for _ in range(MAX_STATUS_CHANGE_TIME_SECONDS // POLL_FREQUENCY_SECONDS):
            await asyncio.sleep(POLL_FREQUENCY_SECONDS)
            if self.coordinator.data.get(self.entity_description.key) == new_mode:
                break
