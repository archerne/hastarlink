"""Config flow for Starlink Statistics and Alerts."""
#from starlinkpypi import Starlink

from homeassistant.helpers import config_entry_flow

from .const import DOMAIN
from . import StarlinkClass


async def _async_has_devices(hass) -> bool:
    """Return if there are devices that can be discovered."""
    api_client = StarlinkClass()

    devices = await api_client.get()
    return len(devices) > 0


config_entry_flow.register_discovery_flow(
    DOMAIN,
    "Starlink Statistics and Alerts",
    _async_has_devices,
)
