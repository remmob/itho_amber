"""Modbus connection for the Itho Amber integration.

Builds a "unit": a handle to one device on a Modbus line. Ownership of the
underlying connection (who opens/closes it, and when) is not this module's
concern - it is either handed off to Home Assistant's shared modbus
connection (2026.9+) or owned by us via modbus_connection (older versions).

This is the same pattern used by sht20, comfoair, magna3 and
deye_hybride_inverter, so the Amber can share a Modbus TCP gateway with
those integrations instead of opening a second competing connection to it.

Unlike those integrations, the Amber only ever talks Modbus TCP (no RS485
variant exists for it), so there is no serial branch here.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from modbus_connection import ModbusTcpParams, ModbusUnit
from modbus_connection.tmodbus import ModbusConnection

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant

from .const import DEFAULT_PORT

# `async_get_unit` lives in Home Assistant's own modbus integration but only
# exists from 2026.9 onward. On older versions this import fails and we fall
# back to our own connection, so one codebase supports both.
#
# Remove this fallback (and raise the floor in hacs.json) around September
# 2027, one year after 2026.9.
try:
    from homeassistant.components.modbus import async_get_unit

    HAS_SHARED_CONNECTION = True
except ImportError:  # Home Assistant older than 2026.9
    async_get_unit = None
    HAS_SHARED_CONNECTION = False


# Labels for the diagnostic sensor that shows which of the two connection
# methods above is active.
METHOD_SHARED = "shared (HA modbus)"
METHOD_OWN = "own connection"


def active_method() -> str:
    """Return which connection method this Home Assistant instance uses."""
    return METHOD_SHARED if HAS_SHARED_CONNECTION else METHOD_OWN


def build_params(data: Mapping[str, Any]) -> ModbusTcpParams:
    """Build the connection parameters from the config entry data.

    This is a description only - no network traffic happens here.
    """
    return ModbusTcpParams(
        host=data[CONF_HOST],
        port=int(data.get(CONF_PORT, DEFAULT_PORT)),
    )


def async_setup_unit(
    hass: HomeAssistant,
    entry: ConfigEntry,
    params: ModbusTcpParams,
    unit_id: int,
) -> ModbusUnit:
    """Return a unit for this config entry.

    On 2026.9+, `async_get_unit` requests a unit from Home Assistant. Two
    integrations talking to the same gateway get a unit on the same
    underlying socket and their requests queue behind each other, which is
    what lets the Amber share a Modbus TCP gateway with other integrations.
    Home Assistant closes the shared connection itself once the last config
    entry releases it.

    On older versions we open our own connection instead. Functionally
    identical, just not shared: every integration keeps its own socket.
    """
    if async_get_unit is not None:
        return async_get_unit(hass, entry, params, unit_id)

    connection = ModbusConnection(params)
    entry.async_on_unload(connection.close)
    return connection.for_unit(unit_id)
