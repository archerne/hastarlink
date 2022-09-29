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

from .const import COORDINATOR, DOMAIN, SPACEX_API

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)
_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["binary_sensor", "sensor"]


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


class StarlinkClass:

    def __init__(self):
        pass

    async def get(self):
        from .dish_grpc_text import DishGrpcText
        _dish_grpc_text = DishGrpcText()

        class Object(object):
            pass
        obj = Object()
        obj.target = None
        obj.numeric = False
        obj.loop_interval = 0.0
        obj.verbose = False,
        obj.samples = -1
        obj.poll_loops = 1
        obj.no_counter = False
        obj.print_header = False
        obj.out_file = '-'
        obj.skip_query = False
        obj.mode = ["status", "alert_detail", "location"]
        obj.status_mode = True
        obj.pure_status_mode = True
        obj.history_stats_mode = False
        obj.bulk_mode = False
        obj.bulk_samples = -1
        obj.no_stdout_errors = True
        obj.need_id = False
        response = _dish_grpc_text.main(obj)
        responseObj = {}
        for line in response:
            atts = line.split(",")
            for x in atts:
                keypair = x.split(":")
                #print(f"Key: '{keypair[0].strip()}' Value: '{keypair[1].strip()}'")
                responseObj[keypair[0].strip()] = keypair[1].strip()
        # print(response)
        return responseObj
