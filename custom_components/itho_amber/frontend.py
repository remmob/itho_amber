"""Serves the integration's own Lovelace cards.

The card ships inside the integration, so there is nothing to install through
HACS and nothing to register as a Lovelace resource by hand. The `frontend`
folder is served as a static path and the module is added to the list Home
Assistant loads on every dashboard, which makes the card type available right
after installation.
"""

from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.components import frontend
from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STATIC_URL = f"/{DOMAIN}_frontend"
CARDS = ["amber-legionella-card.js"]
DATA_FRONTEND_REGISTERED = f"{DOMAIN}_frontend_registered"


def _cache_tag(folder: Path) -> str:
    """Return a tag that changes whenever a card file changes.

    Based on the newest modification time in the folder, so a browser picks up
    an edited card after an integration reload without having to bump a version
    by hand while developing.
    """
    newest = 0.0
    for name in CARDS:
        try:
            newest = max(newest, (folder / name).stat().st_mtime)
        except OSError:
            continue
    return str(int(newest))


async def async_register_frontend(hass: HomeAssistant) -> None:
    """Serve the card files and have Home Assistant load them."""
    # Static paths and extra module URLs cannot be removed again, so guard
    # against a reload registering them twice.
    if hass.data.get(DATA_FRONTEND_REGISTERED):
        return

    folder = Path(__file__).parent / "frontend"
    if not folder.is_dir():
        _LOGGER.warning("Frontend folder %s is missing, cards are not served", folder)
        return

    await hass.http.async_register_static_paths(
        [StaticPathConfig(STATIC_URL, str(folder), cache_headers=False)]
    )

    tag = await hass.async_add_executor_job(_cache_tag, folder)
    for card in CARDS:
        url = f"{STATIC_URL}/{card}?v={tag}"
        frontend.add_extra_js_url(hass, url)
        _LOGGER.debug("Serving card %s", url)

    hass.data[DATA_FRONTEND_REGISTERED] = True
