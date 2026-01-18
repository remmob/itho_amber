import ipaddress
import re
import logging

import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

from homeassistant import config_entries
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
)
from homeassistant.core import HomeAssistant, callback

from .const import (
    DEFAULT_NAME,
    DEFAULT_PORT,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
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
from .repairs import async_migrate_temperature_typo


DATA_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
        
        # === ALARM NOTIFICATIONS (P/F/E/S) ===
        vol.Optional(CONF_NOTIFY_ALARMS_MOBILE, default=DEFAULT_NOTIFY_ALARMS_MOBILE): bool,
        vol.Optional(CONF_NOTIFY_ALARMS_SERVICES, default=DEFAULT_NOTIFY_ALARMS_SERVICES): str,
        vol.Optional(CONF_NOTIFY_ALARMS_PERSISTENT, default=DEFAULT_NOTIFY_ALARMS_PERSISTENT): bool,
        vol.Optional(CONF_ALARM_NOTIFICATION_TITLE, default=DEFAULT_ALARM_NOTIFICATION_TITLE): str,
        vol.Optional(CONF_ALARM_DELAY, default=DEFAULT_ALARM_DELAY): vol.All(vol.Coerce(int), vol.Range(min=60, max=3600)),
        
        # === CONNECTION/INTEGRATION ERRORS ===
        vol.Optional(CONF_NOTIFY_CONNECTION_ERRORS_MOBILE, default=DEFAULT_NOTIFY_CONNECTION_ERRORS_MOBILE): bool,
        vol.Optional(CONF_NOTIFY_CONNECTION_ERRORS_SERVICES, default=DEFAULT_NOTIFY_CONNECTION_ERRORS_SERVICES): str,
        vol.Optional(CONF_NOTIFY_CONNECTION_ERRORS_PERSISTENT, default=DEFAULT_NOTIFY_CONNECTION_ERRORS_PERSISTENT): bool,
        vol.Optional(CONF_CONNECTION_ERROR_NOTIFICATION_TITLE, default=DEFAULT_CONNECTION_ERROR_NOTIFICATION_TITLE): str,
        vol.Optional(CONF_CONNECTION_ERROR_DELAY, default=DEFAULT_CONNECTION_ERROR_DELAY): vol.All(vol.Coerce(int), vol.Range(min=60, max=3600)),
    }
)

def host_valid(host):
    """Return True if hostname or IP address is valid."""
    try:
        if ipaddress.ip_address(host).version in (4, 6):
            return True
    except ValueError:
        disallowed = re.compile(r"[^a-zA-Z\d\-]")
        return all(x and not disallowed.search(x) for x in host.split("."))


@callback
def amber_modbus_entries(hass: HomeAssistant):
    """Return the hosts already configured."""
    return {
        entry.data[CONF_HOST]
        for entry in hass.config_entries.async_entries(DOMAIN)
    }


class AmberModbusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the initial setup flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return AmberOptionsFlowHandler()

    def _host_in_configuration_exists(self, host) -> bool:
        return host in amber_modbus_entries(self.hass)

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]

            if self._host_in_configuration_exists(host):
                errors[CONF_HOST] = "already_configured"
            elif not host_valid(host):
                errors[CONF_HOST] = "invalid_host"
            else:
                await self.async_set_unique_id(host)
                self._abort_if_unique_id_configured()
                
                # Process all the data including new notification settings
                data = {
                    CONF_NAME: user_input.get(CONF_NAME, DEFAULT_NAME),
                    CONF_HOST: host,
                    CONF_PORT: user_input.get(CONF_PORT, DEFAULT_PORT),
                    CONF_SCAN_INTERVAL: user_input.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
                    # Alarm notifications
                    CONF_NOTIFY_ALARMS_MOBILE: user_input.get(CONF_NOTIFY_ALARMS_MOBILE, DEFAULT_NOTIFY_ALARMS_MOBILE),
                    CONF_NOTIFY_ALARMS_PERSISTENT: user_input.get(CONF_NOTIFY_ALARMS_PERSISTENT, DEFAULT_NOTIFY_ALARMS_PERSISTENT),
                    CONF_NOTIFY_ALARMS_SERVICES: user_input.get(CONF_NOTIFY_ALARMS_SERVICES, DEFAULT_NOTIFY_ALARMS_SERVICES),
                    CONF_ALARM_NOTIFICATION_TITLE: user_input.get(CONF_ALARM_NOTIFICATION_TITLE, DEFAULT_ALARM_NOTIFICATION_TITLE),
                    CONF_ALARM_DELAY: int(user_input.get(CONF_ALARM_DELAY, DEFAULT_ALARM_DELAY)),
                    # Connection error notifications
                    CONF_NOTIFY_CONNECTION_ERRORS_MOBILE: user_input.get(CONF_NOTIFY_CONNECTION_ERRORS_MOBILE, DEFAULT_NOTIFY_CONNECTION_ERRORS_MOBILE),
                    CONF_NOTIFY_CONNECTION_ERRORS_PERSISTENT: user_input.get(CONF_NOTIFY_CONNECTION_ERRORS_PERSISTENT, DEFAULT_NOTIFY_CONNECTION_ERRORS_PERSISTENT),
                    CONF_NOTIFY_CONNECTION_ERRORS_SERVICES: user_input.get(CONF_NOTIFY_CONNECTION_ERRORS_SERVICES, DEFAULT_NOTIFY_CONNECTION_ERRORS_SERVICES),
                    CONF_CONNECTION_ERROR_NOTIFICATION_TITLE: user_input.get(CONF_CONNECTION_ERROR_NOTIFICATION_TITLE, DEFAULT_CONNECTION_ERROR_NOTIFICATION_TITLE),
                    CONF_CONNECTION_ERROR_DELAY: int(user_input.get(CONF_CONNECTION_ERROR_DELAY, DEFAULT_CONNECTION_ERROR_DELAY)),
                }
                
                return self.async_create_entry(
                    title=user_input.get(CONF_NAME, DEFAULT_NAME),
                    data=data,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )


class AmberOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Amber Modbus."""

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            _LOGGER.debug(f"Received user_input: {user_input}")
            # Validate the host
            host = user_input.get(CONF_HOST)
            if host and not host_valid(host):
                return self.async_show_form(
                    step_id="init",
                    data_schema=self._get_options_schema(),
                    errors={CONF_HOST: "invalid_host"},
                )
            
            # Validate alarm notify services if alarms mobile is enabled
            notify_alarms_services = user_input.get(CONF_NOTIFY_ALARMS_SERVICES, "").strip()
            if user_input.get(CONF_NOTIFY_ALARMS_MOBILE) and notify_alarms_services:
                # Check if services exist
                services = [s.strip() for s in notify_alarms_services.split(",") if s.strip()]
                invalid_services = []
                for service in services:
                    if not self.hass.services.has_service("notify", service):
                        invalid_services.append(service)
                
                if invalid_services:
                    return self.async_show_form(
                        step_id="init",
                        data_schema=self._get_options_schema(),
                        errors={CONF_NOTIFY_ALARMS_SERVICES: "invalid_notify_service"},
                        description_placeholders={"invalid_services": ", ".join(invalid_services)},
                    )
            
            # Validate connection error notify services if connection errors mobile is enabled
            notify_connection_services = user_input.get(CONF_NOTIFY_CONNECTION_ERRORS_SERVICES, "").strip()
            if user_input.get(CONF_NOTIFY_CONNECTION_ERRORS_MOBILE) and notify_connection_services:
                # Check if services exist
                services = [s.strip() for s in notify_connection_services.split(",") if s.strip()]
                invalid_services = []
                for service in services:
                    if not self.hass.services.has_service("notify", service):
                        invalid_services.append(service)
                
                if invalid_services:
                    return self.async_show_form(
                        step_id="init",
                        data_schema=self._get_options_schema(),
                        errors={CONF_NOTIFY_CONNECTION_ERRORS_SERVICES: "invalid_notify_service"},
                        description_placeholders={"invalid_services": ", ".join(invalid_services)},
                    )
            
            # Ensure delays are integers
            alarm_delay = int(user_input.get(CONF_ALARM_DELAY, DEFAULT_ALARM_DELAY))
            connection_error_delay = int(user_input.get(CONF_CONNECTION_ERROR_DELAY, DEFAULT_CONNECTION_ERROR_DELAY))
            
            # Update the config entry with new data
            # Note: NAME is only editable during initial setup, not in options
            self.hass.config_entries.async_update_entry(
                self.config_entry,
                data={
                    CONF_NAME: self.config_entry.data.get(CONF_NAME, DEFAULT_NAME),
                    CONF_HOST: user_input.get(CONF_HOST, self.config_entry.data.get(CONF_HOST)),
                    CONF_PORT: user_input.get(CONF_PORT, self.config_entry.data.get(CONF_PORT, DEFAULT_PORT)),
                    CONF_SCAN_INTERVAL: user_input.get(CONF_SCAN_INTERVAL, self.config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)),
                    # Alarm notifications
                    CONF_NOTIFY_ALARMS_MOBILE: user_input.get(CONF_NOTIFY_ALARMS_MOBILE, DEFAULT_NOTIFY_ALARMS_MOBILE),
                    CONF_NOTIFY_ALARMS_PERSISTENT: user_input.get(CONF_NOTIFY_ALARMS_PERSISTENT, DEFAULT_NOTIFY_ALARMS_PERSISTENT),
                    CONF_NOTIFY_ALARMS_SERVICES: notify_alarms_services,
                    CONF_ALARM_NOTIFICATION_TITLE: user_input.get(CONF_ALARM_NOTIFICATION_TITLE, DEFAULT_ALARM_NOTIFICATION_TITLE),
                    CONF_ALARM_DELAY: alarm_delay,
                    # Connection error notifications
                    CONF_NOTIFY_CONNECTION_ERRORS_MOBILE: user_input.get(CONF_NOTIFY_CONNECTION_ERRORS_MOBILE, DEFAULT_NOTIFY_CONNECTION_ERRORS_MOBILE),
                    CONF_NOTIFY_CONNECTION_ERRORS_PERSISTENT: user_input.get(CONF_NOTIFY_CONNECTION_ERRORS_PERSISTENT, DEFAULT_NOTIFY_CONNECTION_ERRORS_PERSISTENT),
                    CONF_NOTIFY_CONNECTION_ERRORS_SERVICES: notify_connection_services,
                    CONF_CONNECTION_ERROR_NOTIFICATION_TITLE: user_input.get(CONF_CONNECTION_ERROR_NOTIFICATION_TITLE, DEFAULT_CONNECTION_ERROR_NOTIFICATION_TITLE),
                    CONF_CONNECTION_ERROR_DELAY: connection_error_delay,
                }
            )
            # Reload the integration to apply changes
            await self.hass.config_entries.async_reload(self.config_entry.entry_id)
            return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="init",
            data_schema=self._get_options_schema(),
        )
    
    def _get_options_schema(self):
        """Return the options schema."""
        # Note: NAME field is NOT included in options - only editable during initial setup
        return vol.Schema(
            {
                # Connection settings
                vol.Required(
                    CONF_HOST,
                    default=self.config_entry.data.get(CONF_HOST)
                ): str,
                vol.Required(
                    CONF_PORT,
                    default=self.config_entry.data.get(CONF_PORT, DEFAULT_PORT)
                ): int,
                vol.Optional(
                    CONF_SCAN_INTERVAL,
                    default=self.config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
                ): int,
                
                # === ALARM NOTIFICATIONS (P/F/E/S) ===
                vol.Optional(
                    CONF_NOTIFY_ALARMS_MOBILE,
                    default=self.config_entry.data.get(CONF_NOTIFY_ALARMS_MOBILE, DEFAULT_NOTIFY_ALARMS_MOBILE)
                ): bool,
                vol.Optional(
                    CONF_NOTIFY_ALARMS_SERVICES,
                    default=self.config_entry.data.get(CONF_NOTIFY_ALARMS_SERVICES, DEFAULT_NOTIFY_ALARMS_SERVICES),
                    description={"suggested_value": self.config_entry.data.get(CONF_NOTIFY_ALARMS_SERVICES, DEFAULT_NOTIFY_ALARMS_SERVICES)}
                ): str,
                vol.Optional(
                    CONF_NOTIFY_ALARMS_PERSISTENT,
                    default=self.config_entry.data.get(CONF_NOTIFY_ALARMS_PERSISTENT, DEFAULT_NOTIFY_ALARMS_PERSISTENT)
                ): bool,
                vol.Optional(
                    CONF_ALARM_NOTIFICATION_TITLE,
                    default=self.config_entry.data.get(CONF_ALARM_NOTIFICATION_TITLE, DEFAULT_ALARM_NOTIFICATION_TITLE)
                ): str,
                vol.Optional(
                    CONF_ALARM_DELAY,
                    default=self.config_entry.data.get(CONF_ALARM_DELAY, DEFAULT_ALARM_DELAY)
                ): vol.All(vol.Coerce(int), vol.Range(min=60, max=3600)),
                
                # === CONNECTION/INTEGRATION ERRORS ===
                vol.Optional(
                    CONF_NOTIFY_CONNECTION_ERRORS_MOBILE,
                    default=self.config_entry.data.get(CONF_NOTIFY_CONNECTION_ERRORS_MOBILE, DEFAULT_NOTIFY_CONNECTION_ERRORS_MOBILE)
                ): bool,
                vol.Optional(
                    CONF_NOTIFY_CONNECTION_ERRORS_SERVICES,
                    default=self.config_entry.data.get(CONF_NOTIFY_CONNECTION_ERRORS_SERVICES, DEFAULT_NOTIFY_CONNECTION_ERRORS_SERVICES),
                    description={"suggested_value": self.config_entry.data.get(CONF_NOTIFY_CONNECTION_ERRORS_SERVICES, DEFAULT_NOTIFY_CONNECTION_ERRORS_SERVICES)}
                ): str,
                vol.Optional(
                    CONF_NOTIFY_CONNECTION_ERRORS_PERSISTENT,
                    default=self.config_entry.data.get(CONF_NOTIFY_CONNECTION_ERRORS_PERSISTENT, DEFAULT_NOTIFY_CONNECTION_ERRORS_PERSISTENT)
                ): bool,
                vol.Optional(
                    CONF_CONNECTION_ERROR_NOTIFICATION_TITLE,
                    default=self.config_entry.data.get(CONF_CONNECTION_ERROR_NOTIFICATION_TITLE, DEFAULT_CONNECTION_ERROR_NOTIFICATION_TITLE)
                ): str,
                vol.Optional(
                    CONF_CONNECTION_ERROR_DELAY,
                    default=self.config_entry.data.get(CONF_CONNECTION_ERROR_DELAY, DEFAULT_CONNECTION_ERROR_DELAY)
                ): vol.All(vol.Coerce(int), vol.Range(min=60, max=3600)),
            }
        )

