"""The Amber Integration."""

from __future__ import annotations

import logging
import asyncio

import voluptuous as vol
from homeassistant.const import __version__
import homeassistant.helpers.config_validation as cv
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
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
REQUIRED_VERSION = "2025.6.0"

def check_homeassistant_version():
    if __version__ < REQUIRED_VERSION:
        raise ValueError(f"Deze integratie vereist Home Assistant {REQUIRED_VERSION} of hoger.")

check_homeassistant_version()

async def async_setup(_hass: HomeAssistant, _config: dict) -> bool:
    """Set up this integration using YAML is not supported."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up an Amber Modbus integration using UI."""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    name = entry.data.get("name")
    host = entry.data.get("host")
    port = entry.data.get("port")
    scan_interval = entry.data.get("scan_interval")

    _LOGGER.info("Setting up %s.%s", DOMAIN, name)

    if name in hass.data[DOMAIN]:
        _LOGGER.warning("Config entry %s is already set up!", name)
        return False

    hub = AmberModbusHub(hass, name, host, port, scan_interval)
    await hub.async_config_entry_first_refresh()

    hass.data[DOMAIN][name] = {"hub": hub}

    for component in PLATFORMS:
        await hass.config_entries.async_forward_entry_setups(entry, [component])

    _LOGGER.info("Integration setup completed successfully!")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Amber Modbus entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    
    if unload_ok:
        name = entry.data.get(CONF_NAME)
        if name in hass.data[DOMAIN]:
            hass.data[DOMAIN].pop(name)

    return unload_ok
