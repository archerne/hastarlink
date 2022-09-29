"""Definition and setup of the Starlink Buttons for Home Assistant."""
import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import ATTR_NAME

from . import StarlinkUpdateCoordinator
from .const import ATTR_IDENTIFIERS, ATTR_MANUFACTURER, ATTR_MODEL, DOMAIN, COORDINATOR

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up buttons."""
    coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]
    buttons = []

    buttons.append(
        StarlinkButton(
            coordinator,
            "Dish Reboot",
            "starlink_reboot",
            "mdi:restart",
            "starlinkstats"))

    buttons.append(
        StarlinkButton(
            coordinator,
            "Dish Stow",
            "starlink_stow",
            "mdi:inbox-arrow-down-outline",
            "starlinkstats"))

    buttons.append(
        StarlinkButton(
            coordinator,
            "Dish Unstow",
            "starlink_unstow",
            "mdi:satellite-uplink",
            "starlinkstats"))

    async_add_entities(buttons)


class StarlinkButton(ButtonEntity):
    """Represent an button."""

    def __init__(
        self,
        coordinator: StarlinkUpdateCoordinator,
        name: str,
        entity_id: str,
        icon: str,
        device_identifier: str,
    ):
        """Initialize Entities."""
        self._name = name
        self._unique_id = f"starlink_{entity_id}"
        self._state = None
        self._icon = icon
        self._kind = entity_id
        self._device_identifier = device_identifier
        self.coordinator = coordinator
        self.attrs = {}

    @property
    def unique_id(self):
        """Return the unique Home Assistant friendly identifier for this entity."""
        return self._unique_id

    @property
    def name(self):
        """Return the friendly name of this entity."""
        return self._name

    @property
    def icon(self):
        """Return the icon for this entity."""
        return self._icon

    @property
    def extra_state_attributes(self):
        """Return the attributes."""

        return self.attrs

    @property
    def device_info(self):
        """Define the device based on device_identifier."""

        device_name = "Starlink Stats"
        device_model = "Stats"

        return {
            ATTR_IDENTIFIERS: {(DOMAIN, self._device_identifier)},
            ATTR_NAME: device_name,
            ATTR_MANUFACTURER: "Starlink",
            ATTR_MODEL: device_model,
        }

    async def async_press(self):
        """Handle the button press."""

        if self._kind == "starlink_reboot":
            await self.coordinator.reboot_job()
            _LOGGER.debug("Rebooting dish.")

        elif self._kind == "starlink_stow":
            await self.coordinator.stow_job()
            _LOGGER.debug("Stowing dish.")

        elif self._kind == "starlink_unstow":
            await self.coordinator.unstow_job()
            _LOGGER.debug("Unstowing dish.")

    async def async_added_to_hass(self):
        """Subscribe to updates."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
