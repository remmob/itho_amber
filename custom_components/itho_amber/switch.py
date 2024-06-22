"""Platform for switch integration."""

from __future__ import annotations
#from datetime import datetime
import asyncio
#import time
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.switch import SwitchEntity

from homeassistant.const import CONF_NAME
from homeassistant.core import callback
#from homeassistant.helpers.typing import HomeAssistantType
import homeassistant.util.dt as dt_util

from .const import (
    ATTR_MANUFACTURER,
    DOMAIN,
    SWITCH_TYPES,
    AmberModbusSwitchEntityDescription,
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
    for switch_description in SWITCH_TYPES.values():
        switch = AmberSwitch(
            hub_name,
            hub,
            device_info,
            switch_description,
        )
        entities.append(switch)

    async_add_entities(entities)

    return True

class AmberSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a Amber Modbus switch."""

    POLL_FREQUENCY_SECONDS = 15
    MAX_STATUS_CHANGE_TIME_SECONDS = 30 #Todo: make this dependend on main poll intervall

    def __init__(
        self,
        platform_name: str,
        hub: AmberModbusHub,
        device_info,
        description: AmberModbusSwitchEntity,

    ):
        """Initialize the switch."""
        self._platform_name = platform_name
        self._attr_device_info = device_info
        self.entity_description: AmberModbusSwitchEntity = description
        self._hub = hub

        super().__init__(coordinator=hub)
        self._attr_is_on = self.coordinator.data[self.entity_description.key]

    @callback
    def _handle_coordinator_update(self) -> None:
        self._attr_is_on = self.coordinator.data[self.entity_description.key]
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name."""
        return f"{self._platform_name} {self.entity_description.name}"

    @property
    def unique_id(self) -> Optional[str]:
        return f"{self._platform_name}_{self.entity_description.key}"

    async def async_turn_on(self, **kwargs):
        """Send the on command."""
        address = int(self.entity_description.key)
        self._hub.write_registers(address, 1)

        for _ in range(
                self.MAX_STATUS_CHANGE_TIME_SECONDS // self.POLL_FREQUENCY_SECONDS
            ):
                await asyncio.sleep(self.POLL_FREQUENCY_SECONDS)
                
                if not self.coordinator.data[self.entity_description.key]:
                    self._attr_is_on = True
                    break
        
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Send the off command."""
        address = int(self.entity_description.key)
        self._hub.write_registers(address, 0)
        for _ in range(
                self.MAX_STATUS_CHANGE_TIME_SECONDS // self.POLL_FREQUENCY_SECONDS
            ):
                await asyncio.sleep(self.POLL_FREQUENCY_SECONDS)
                
                if not self.coordinator.data[self.entity_description.key]:
                    self._attr_is_on = False
                    break
        
        await self.coordinator.async_request_refresh()