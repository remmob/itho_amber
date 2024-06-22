"""platform for number integration"""

from __future__ import annotations
#from datetime import datetime
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.number import NumberEntity

from homeassistant.const import CONF_NAME
#from homeassistant.core import callback
import homeassistant.util.dt as dt_util
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder

from .const import (
    ATTR_MANUFACTURER,
    DOMAIN,
    NUMBER_TYPES,
    AmberModbusNumberEntityDescription,
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
    for number_description in NUMBER_TYPES.values():
        number = AmberNumber(
            hub_name,
            hub,
            device_info,
            number_description,
        )
        entities.append(number)

    async_add_entities(entities)

    return True

class AmberNumber(CoordinatorEntity, NumberEntity):
    """Representation of a Amber Modbus number."""

    should_poll = False

    def __init__(
        self,
        platform_name: str,
        hub: AmberModbusHub,
        device_info,
        description: AmberModbusNumberEntityDescription,
    ):
        """Initialize the sensor."""
        self._platform_name = platform_name
        self._attr_device_info = device_info
        self.entity_description: AmberModbusNumberEntityDescription = description
        self._hub = hub

        super().__init__(coordinator=hub)

    @property
    def name(self):
        """Return the name."""
        return f"{self._platform_name} {self.entity_description.name}"

    @property
    def unique_id(self) -> Optional[str]:
        return f"{self._platform_name}_{self.entity_description.key}"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return (
            self.coordinator.data[self.entity_description.key]
            if self.entity_description.key in self.coordinator.data
            else None
        ) 

    @property
    def native_max_value(self) -> int:
        """Set max settable value."""
        max_value = self.entity_description.native_max_value
        return max_value

    @property
    def native_min_value(self) -> int:
        """Set min settable value."""
        min_value = self.entity_description.native_min_value 
        return  min_value  

    def set_native_value(self, value: int) -> None:
        """Set new value and write to modbus."""
        address = int(self.entity_description.key)
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG)
        builder.add_16bit_int(int(value))
        self._hub.write_registers(address, payload=builder.to_registers())