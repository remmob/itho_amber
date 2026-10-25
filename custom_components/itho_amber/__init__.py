"""The Amber Integration."""

from __future__ import annotations

from homeassistant.components.persistent_notification import async_create
from homeassistant.helpers.translation import async_get_translations
from importlib.metadata import version as get_version
from packaging.version import Version

import logging
import asyncio

import voluptuous as vol
from homeassistant.const import __version__
import homeassistant.helpers.config_validation as cv
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import device_registry as dr

from . import connection
from .frontend import async_register_frontend
from .repairs import async_migrate_long_entity_ids, async_migrate_temperature_typo

from .const import (
    DOMAIN,
    DEFAULT_NAME,
    LEGIONELLA_DAYS,
    SERVICE_SET_LEGIONELLA_SCHEDULE,
    DEFAULT_SCAN_INTERVAL,
    # New notification config
    CONF_NOTIFY_ALARMS_MOBILE,
    CONF_NOTIFY_ALARMS_PERSISTENT,
    CONF_NOTIFY_ALARMS_SERVICES,
    CONF_ALARM_NOTIFICATION_TITLE,
    CONF_ALARM_DELAY,
    CONF_NOTIFY_CONNECTION_ERRORS_MOBILE,
    CONF_NOTIFY_CONNECTION_ERRORS_PERSISTENT,
    CONF_NOTIFY_CONNECTION_ERRORS_SERVICES,
    CONF_CONNECTION_ERROR_NOTIFICATION_TITLE,
    CONF_CONNECTION_ERROR_DELAY,
    # Defaults
    DEFAULT_NOTIFY_ALARMS_MOBILE,
    DEFAULT_NOTIFY_ALARMS_PERSISTENT,
    DEFAULT_NOTIFY_ALARMS_SERVICES,
    DEFAULT_ALARM_NOTIFICATION_TITLE,
    DEFAULT_ALARM_DELAY,
    DEFAULT_NOTIFY_CONNECTION_ERRORS_MOBILE,
    DEFAULT_NOTIFY_CONNECTION_ERRORS_PERSISTENT,
    DEFAULT_NOTIFY_CONNECTION_ERRORS_SERVICES,
    DEFAULT_CONNECTION_ERROR_NOTIFICATION_TITLE,
    DEFAULT_CONNECTION_ERROR_DELAY,
)

from .hub import AmberModbusHub
from .alarm_monitor import AlarmMonitor

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
    scan_interval = entry.data.get("scan_interval")
    
    # Connection error notification settings
    notify_connection_errors_mobile = entry.data.get(CONF_NOTIFY_CONNECTION_ERRORS_MOBILE, DEFAULT_NOTIFY_CONNECTION_ERRORS_MOBILE)
    notify_connection_errors_persistent = entry.data.get(CONF_NOTIFY_CONNECTION_ERRORS_PERSISTENT, DEFAULT_NOTIFY_CONNECTION_ERRORS_PERSISTENT)
    notify_connection_errors_services = entry.data.get(CONF_NOTIFY_CONNECTION_ERRORS_SERVICES, DEFAULT_NOTIFY_CONNECTION_ERRORS_SERVICES)
    connection_error_notification_title = entry.data.get(CONF_CONNECTION_ERROR_NOTIFICATION_TITLE, DEFAULT_CONNECTION_ERROR_NOTIFICATION_TITLE)
    connection_error_delay = entry.data.get(CONF_CONNECTION_ERROR_DELAY, DEFAULT_CONNECTION_ERROR_DELAY)
    
    # Alarm notification settings
    notify_alarms_mobile = entry.data.get(CONF_NOTIFY_ALARMS_MOBILE, DEFAULT_NOTIFY_ALARMS_MOBILE)
    notify_alarms_persistent = entry.data.get(CONF_NOTIFY_ALARMS_PERSISTENT, DEFAULT_NOTIFY_ALARMS_PERSISTENT)
    notify_alarms_services = entry.data.get(CONF_NOTIFY_ALARMS_SERVICES, DEFAULT_NOTIFY_ALARMS_SERVICES)
    alarm_notification_title = entry.data.get(CONF_ALARM_NOTIFICATION_TITLE, DEFAULT_ALARM_NOTIFICATION_TITLE)
    alarm_delay = entry.data.get(CONF_ALARM_DELAY, DEFAULT_ALARM_DELAY)
    
    _LOGGER.debug(f"Connection error delay configured: {connection_error_delay} seconds")
    _LOGGER.debug(f"Alarm delay configured: {alarm_delay} seconds")

    _LOGGER.info("Setting up %s.%s", DOMAIN, name)
    _LOGGER.debug(f"Required Home Assistant version: {REQUIRED_VERSION}")
    _LOGGER.debug(f"Detected Home Assistant version: {ha_version}")

    if name in hass.data[DOMAIN]:
        _LOGGER.warning("Config entry %s is already set up!", name)
        return False

    params = connection.build_params(entry.data)
    unit = connection.async_setup_unit(hass, entry, params, unit_id=1)
    _LOGGER.info("%s is using connection method: %s", name, connection.active_method())

    hub = AmberModbusHub(hass, name, unit, scan_interval, notify_connection_errors_mobile, notify_connection_errors_persistent, notify_connection_errors_services, connection_error_notification_title, connection_error_delay)
    await hub.async_config_entry_first_refresh()

    # Create alarm monitor
    alarm_monitor = AlarmMonitor(hass, name, notify_alarms_mobile, notify_alarms_persistent, notify_alarms_services, alarm_notification_title, alarm_delay)

    hass.data[DOMAIN][name] = {"hub": hub, "alarm_monitor": alarm_monitor}

    for component in PLATFORMS:
        await hass.config_entries.async_forward_entry_setups(entry, [component])

    # Start alarm monitoring after all entities are set up
    alarm_monitor.start_monitoring()

    _async_register_services(hass)

    # Serve the integration's own Lovelace cards. A failure here must not stop
    # the heat pump from working, so it is logged and shrugged off.
    try:
        await async_register_frontend(hass)
    except Exception as err:
        _LOGGER.error("Could not register the frontend cards: %s", err)

    # Perform migration automatically 
    try:
        changed = await async_migrate_temperature_typo(hass)
        changed = await async_migrate_long_entity_ids(hass) or changed
        if changed:
            _LOGGER.info("Automatic entity ID migration completed successfully.")
    except Exception as err:
        _LOGGER.error("Automatic entity ID migration failed: %s", err)

    _LOGGER.info("Integration setup completed successfully!")

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Amber Modbus entry."""
    name = entry.data.get(CONF_NAME)
    
    # Stop alarm monitoring
    if name in hass.data[DOMAIN]:
        alarm_monitor = hass.data[DOMAIN][name].get("alarm_monitor")
        if alarm_monitor:
            alarm_monitor.stop_monitoring()
    
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    
    if unload_ok:
        if name in hass.data[DOMAIN]:
            hass.data[DOMAIN].pop(name)

        # Drop the actions once the last hub is gone, otherwise they would be
        # offered in the UI without anything behind them.
        if not hass.data[DOMAIN]:
            hass.services.async_remove(DOMAIN, SERVICE_SET_LEGIONELLA_SCHEDULE)

    return unload_ok


SET_LEGIONELLA_SCHEDULE_SCHEMA = vol.Schema(
    {
        vol.Required("days"): vol.All(cv.ensure_list, [vol.In(LEGIONELLA_DAYS)]),
        vol.Required("time"): cv.time,
        vol.Optional("device_id"): vol.All(cv.ensure_list, [cv.string]),
    }
)


def _resolve_hub(hass: HomeAssistant, device_id: str | None):
    """Return the hub this action should act on.

    With a single Amber there is nothing to choose, so `device_id` may be left
    out. With more than one it is required, and it is resolved through the
    device registry because that is what the UI hands us.
    """
    hubs = hass.data.get(DOMAIN, {})
    if not hubs:
        raise HomeAssistantError("No Amber heat pump is set up")

    if device_id is None:
        if len(hubs) > 1:
            raise HomeAssistantError(
                "More than one Amber heat pump is set up, so a device must be selected"
            )
        return next(iter(hubs.values()))["hub"]

    device = dr.async_get(hass).async_get(device_id)
    if device is None:
        raise HomeAssistantError(f"Unknown device {device_id}")

    for domain, hub_name in device.identifiers:
        if domain == DOMAIN and hub_name in hubs:
            return hubs[hub_name]["hub"]

    raise HomeAssistantError(f"Device {device_id} is not an Amber heat pump")


@callback
def _async_register_services(hass: HomeAssistant) -> None:
    """Register the integration actions once."""
    if hass.services.has_service(DOMAIN, SERVICE_SET_LEGIONELLA_SCHEDULE):
        return

    async def async_set_legionella_schedule(call: ServiceCall) -> None:
        """Write the legionella day mask and start time in one go."""
        days = call.data["days"]
        start = call.data["time"]

        # A target in the UI arrives as a list; without one there has to be a
        # single heat pump and _resolve_hub falls back to it.
        device_ids = call.data.get("device_id") or [None]
        for device_id in device_ids:
            hub = _resolve_hub(hass, device_id)
            mask = hub.encode_legionella_days(days)
            hub.write_legionella_schedule(mask, start.hour, start.minute)
            _LOGGER.info(
                "Legionella schedule set to %s at %02d:%02d",
                ", ".join(days) or "no days",
                start.hour,
                start.minute,
            )

    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_LEGIONELLA_SCHEDULE,
        async_set_legionella_schedule,
        schema=SET_LEGIONELLA_SCHEDULE_SCHEMA,
    )
