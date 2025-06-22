import ipaddress
import re

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import (CONF_HOST, CONF_NAME, CONF_PORT,
                                 CONF_SCAN_INTERVAL)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.selector import TextSelector

from .const import DEFAULT_NAME, DEFAULT_PORT, DEFAULT_SCAN_INTERVAL, DOMAIN
from .hub import AmberModbusHub


DATA_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
    }
)

def host_valid(host):
    """Return True if hostname or IP address is valid."""
    try:
        if ipaddress.ip_address(host).version == (4 or 6):
            return True
    except ValueError:
        disallowed = re.compile(r"[^a-zA-Z\d\-]")
        return all(x and not disallowed.search(x) for x in host.split("."))

@callback
def amber_modbus_entries(hass: HomeAssistant):
    """Return the hosts already configured."""
    return set(
        entry.data[CONF_HOST] for entry in hass.config_entries.async_entries(DOMAIN)
    )

class AmberModbusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Amber Modbus configflow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def _host_in_configuration_exists(self, host) -> bool:
        """Return True if host exists in configuration."""
        if host in amber_modbus_entries(self.hass):
            return True
        return False

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]

            if self._host_in_configuration_exists(host):
                errors[CONF_HOST] = "already_configured"
            elif not host_valid(user_input[CONF_HOST]):
                errors[CONF_HOST] = "invalid host IP"
            else:
                await self.async_set_unique_id(user_input[CONF_HOST])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

    # async def async_step_reconfigure(self, user_input=None):
    #     """Handle reconfiguration of the integration."""
    #     errors = {}

    #     if user_input:
    #         host = user_input[CONF_HOST]
    #         port = user_input[CONF_PORT]
    #         scan_interval = user_input[CONF_SCAN_INTERVAL]

    #         # Validatie van de nieuwe configuratie
    #         hub = AmberModbusHub(self.hass, "Test", host, port, scan_interval)
    #         try:
    #             await hub.async_test_connection()
    #         except Exception:
    #             errors["base"] = "cannot_connect"
    #         else:
    #             entry = self._get_reconfigure_entry()
    #             return self.async_update_reload_and_abort(entry, data_updates=user_input)

    #     return self.async_show_form(
    #         step_id="reconfigure",
    #         data_schema=vol.Schema({
    #             vol.Required(CONF_HOST, default=self.config_entry.data[CONF_HOST]): TextSelector(),
    #             vol.Required(CONF_PORT, default=self.config_entry.data[CONF_PORT]): TextSelector(),
    #             vol.Optional(CONF_SCAN_INTERVAL, default=self.config_entry.data[CONF_SCAN_INTERVAL]): vol.Coerce(int),
    #         }),
    #         errors=errors,
    #     )