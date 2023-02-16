"""The Starlink integration."""
import asyncio
from datetime import timedelta
import logging
#from starlinkpypi import Starlink
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.const import Platform
from .const import COORDINATOR, DOMAIN, SPACEX_API

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)
_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.BINARY_SENSOR, Platform.BUTTON, Platform.SENSOR]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Starlink component."""
    hass.data.setdefault(DOMAIN, {})

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Starlink from a config entry."""
    polling_interval = 1
    api = StarlinkClass()

    try:
        await api.get()
    except ConnectionError as error:
        _LOGGER.debug("Starlink API Error: %s", error)
        return False
        raise ConfigEntryNotReady from error
    except ValueError as error:
        _LOGGER.debug("Starlink API Error: %s", error)
        return False
        raise ConfigEntryNotReady from error

    coordinator = StarlinkUpdateCoordinator(
        hass,
        api=api,
        name="Starlink",
        polling_interval=polling_interval,
    )

    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = {
        COORDINATOR: coordinator, SPACEX_API: api}

    for component in PLATFORMS:
        _LOGGER.info("Setting up platform: %s", component)
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(
                    entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class StarlinkUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching update data from the Starlink endpoint."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: str,
        name: str,
        polling_interval: int,
    ):
        """Initialize the global Starlink data updater."""
        self.api = api

        super().__init__(
            hass=hass,
            logger=_LOGGER,
            name=name,
            update_interval=timedelta(seconds=polling_interval),
        )

    async def _async_update_data(self):
        """Fetch data from Starlink."""
        try:
            _LOGGER.debug("Updating the coordinator data.")
            starlink_data = await self.api.get()

            return starlink_data
        except ConnectionError as error:
            _LOGGER.info("Starlink API: %s", error)
            raise UpdateFailed from error
        except ValueError as error:
            _LOGGER.info("Starlink API: %s", error)
            raise UpdateFailed from error

    async def reboot_job(self):
        try:
            _LOGGER.debug("Rebooting dish.")
            await self.api.reboot_job()
        except Exception as error:
            _LOGGER.info("Starlink API: %s", error)
            raise UpdateFailed from error

    async def stow_job(self):
        try:
            _LOGGER.debug("Rebooting dish.")
            await self.api.stow_job()
        except Exception as error:
            _LOGGER.info("Starlink API: %s", error)
            raise UpdateFailed from error

    async def unstow_job(self):
        try:
            _LOGGER.debug("Rebooting dish.")
            await self.api.unstow_job()
        except Exception as error:
            _LOGGER.info("Starlink API: %s", error)
            raise UpdateFailed from error


class StarlinkClass:

    def __init__(self):
        pass

    async def get(self):
        import starlink_grpc
        status = starlink_grpc.status_data()
        location = starlink_grpc.location_data()
        responseObj = {}
        for line in status:
            responseObj =responseObj | line
        responseObj =responseObj | location
        if responseObj["latitude"] is None or responseObj["latitude"] == '':
            responseObj["latitude"] = 0
        if responseObj["longitude"] is None or responseObj["longitude"] == '':
            responseObj["longitude"] = 0
        if responseObj["altitude"] is None or responseObj["altitude"] == '':
            responseObj["altitude"] = 0

        return responseObj

    async def reboot_job(self):
        import starlink_grpc
        starlink_grpc.reboot()
        return

    async def stow_job(self):
        import starlink_grpc
        starlink_grpc.set_stow_state(unstow=False)
        return

    async def unstow_job(self):
        import starlink_grpc
        starlink_grpc.set_stow_state(unstow=True)
        return
