"""The Amber Integration."""

from __future__ import annotations

import logging
import asyncio

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,
    DEFAULT_NAME,
    DEFAULT_SCAN_INTERVAL,
    )

from .hub import AmberModbusHub

_LOGGER = logging.getLogger(__name__)

AMBER_MODBUS_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PORT): cv.string,
        vol.Optional(
            CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
        ): cv.positive_int,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.Schema({cv.slug: AMBER_MODBUS_SCHEMA})}, extra=vol.ALLOW_EXTRA
)

PLATFORMS = ["sensor", "switch", "number", "select"]

async def async_setup(_hass: HomeAssistant, _config: Config) -> bool:
    """Set up this integration using YAML is not supported."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up a Amber modbus integration using UI."""
    hass.data[DOMAIN] = {}

    host = entry.data[CONF_HOST]
    name = entry.data[CONF_NAME]
    port = entry.data[CONF_PORT]
    scan_interval = entry.data[CONF_SCAN_INTERVAL]
    
    _LOGGER.debug("Setup %s.%s", DOMAIN, name)

    hub = AmberModbusHub(hass, name, host, port, scan_interval)
    await hub.async_config_entry_first_refresh()

    """Register the hub."""
    hass.data[DOMAIN][name] = {"hub": hub}

    for component in PLATFORMS:
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass, entry):
    """Unload Amber mobus entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if not unload_ok:
        return False

    hass.data[DOMAIN].pop(entry.data["name"])
    return True