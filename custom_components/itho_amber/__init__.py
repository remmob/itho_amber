"""The Amber Integration."""

from __future__ import annotations

from homeassistant.components.persistent_notification import async_create
from homeassistant.helpers.translation import async_get_translations
from importlib.metadata import version as get_version
from packaging.version import Version

import pymodbus
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
REQUIRED_VERSION = Version("2025.10.0")

async def async_setup(_hass: HomeAssistant, _config: dict) -> bool:
    """Set up this integration using YAML is not supported."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up an Amber Modbus integration using UI."""
    # Check minimum version Home Assistant
    try:
        ha_version = await hass.async_add_executor_job(lambda: Version(get_version("homeassistant")))
        if ha_version < REQUIRED_VERSION:
            raise RuntimeError(
                f"This integration requires Home Assistant {REQUIRED_VERSION} or higher. Detected version: {ha_version}"
            )

    except Exception as err:
        await async_create(
            hass,
            title="Itho Amber Integration Error",
            message=(
                f"🚫 **Itho Amber integration could not be loaded.**\n\n"
                f"Required version: `{REQUIRED_VERSION}`\n"
                f"Detected version: `{ha_version if 'ha_version' in locals() else 'unknown'}`\n\n"
                f"Error: `{err}`\n\n"
                "🔧 Please update Home Assistant to activate this integration."
            ),
            notification_id="itho_amber_version_blocked"
        )
        return False

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    name = entry.data.get("name")
    host = entry.data.get("host")
    port = entry.data.get("port")
    scan_interval = entry.data.get("scan_interval")

    _LOGGER.info("Setting up %s.%s", DOMAIN, name)
    _LOGGER.debug(f"Used pymodbus version: {pymodbus.__version__}")
    _LOGGER.debug(f"Required Home Assistant version: {REQUIRED_VERSION}")
    _LOGGER.debug(f"Detected Home Assistant version: {ha_version}")

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
