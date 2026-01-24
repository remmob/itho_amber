"""Platform for sensor integration."""

from __future__ import annotations
import logging
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
import homeassistant.util.dt as dt_util

from .const import (
    ATTR_MANUFACTURER,
    DOMAIN,
    SENSOR_TYPES,
    AmberModbusSensorEntityDescription,
    DEFAULT_NAME,
    ATTR_COPYRIGHT,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    hub_name = entry.data[CONF_NAME]
    hub = hass.data[DOMAIN][hub_name]["hub"]

    device_info = {
        "identifiers": {(DOMAIN, hub_name)},
        "name": DEFAULT_NAME,
        "manufacturer": ATTR_MANUFACTURER,
        "model": ATTR_COPYRIGHT,
    }

    entities = []
    for sensor_description in SENSOR_TYPES.values():
        sensor = AmberSensor(
            hub_name,
            hub,
            device_info,
            sensor_description,
        )
        entities.append(sensor)

    async_add_entities(entities)
    return True

class AmberSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Amber Modbus sensor."""

    def __init__(
        self,
        platform_name: str,
        hub: AmberModbusHub,
        device_info,
        description: AmberModbusSensorEntityDescription,
    ):
        """Initialize the sensor."""
        self._platform_name = platform_name
        self._attr_device_info = device_info
        self.entity_description: AmberModbusSensorEntityDescription = description

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
        if self.entity_description.key not in self.coordinator.data:
            return None
        
        value = self.coordinator.data[self.entity_description.key]
        
        # Filter values outside of configured min/max range
        if value is not None:
            if self.entity_description.native_min_value is not None:
                if value < self.entity_description.native_min_value:
                    _LOGGER.debug(
                        f"{self.name}: Value {value} below minimum {self.entity_description.native_min_value}, ignoring"
                    )
                    return self._attr_native_value  # Keep previous value
            
            if self.entity_description.native_max_value is not None:
                if value > self.entity_description.native_max_value:
                    _LOGGER.debug(
                        f"{self.name}: Value {value} above maximum {self.entity_description.native_max_value}, ignoring"
                    )
                    return self._attr_native_value  # Keep previous value
        
        return value 