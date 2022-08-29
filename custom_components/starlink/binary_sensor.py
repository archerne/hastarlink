"""Definition and setup of the Starlink Binary Sensors for Home Assistant."""

import logging
import time

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.const import ATTR_NAME
from homeassistant.components.sensor import ENTITY_ID_FORMAT
from . import StarlinkUpdateCoordinator
from .const import ATTR_IDENTIFIERS, ATTR_MANUFACTURER, ATTR_MODEL, DOMAIN, COORDINATOR

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the binary sensor platforms."""

    coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]
    sensors = []

    sensors.append(
        StarlinkBinarySensor(
            coordinator,
            "Obstructed",
            "starlink_currently_obstructed",
            "mdi:sign-caution",
            "starlinkalert",
        )
    )

    sensors.append(
        StarlinkBinarySensor(
            coordinator,
            "Motors Stuck",
            "starlink_alert_motors_stuck",
            "mdi:engine-off-outline",
            "starlinkalert",
        )
    )

    sensors.append(
        StarlinkBinarySensor(
            coordinator,
            "Thermal Throttle",
            "starlink_alert_thermal_throttle",
            "mdi:thermometer-minus",
            "starlinkalert",
        )
    )
    sensors.append(
        StarlinkBinarySensor(
            coordinator,
            "Thermal Shutdown",
            "starlink_alert_thermal_shutdown",
            "mdi:thermometer-off",
            "starlinkalert",
        )
    )
    sensors.append(
        StarlinkBinarySensor(
            coordinator,
            "Mast Not Near Vertical",
            "starlink_alert_mast_not_near_vertical",
            "mdi:arrow-expand-vertical",
            "starlinkalert",
        )
    )
    sensors.append(
        StarlinkBinarySensor(
            coordinator,
            "Unexpected Location",
            "starlink_alert_unexpected_location",
            "mdi:map-marker-remove-outline",
            "starlinkalert",
        )
    )
    sensors.append(
        StarlinkBinarySensor(
            coordinator,
            "Slow Ethernet Speeds",
            "starlink_alert_slow_ethernet_speeds",
            "mdi:speedometer-slow",
            "starlinkalert",
        )
    )
    sensors.append(
        StarlinkBinarySensor(
            coordinator,
            "Roaming",
            "starlink_alert_roaming",
            "mdi:broadcast-off",
            "starlinkalert",
        )
    )
    sensors.append(
        StarlinkBinarySensor(
            coordinator,
            "Install Pending",
            "starlink_alert_install_pending",
            "mdi:lan-pending",
            "starlinkalert",
        )
    )
    sensors.append(
        StarlinkBinarySensor(
            coordinator,
            "Is Heating",
            "starlink_alert_is_heating",
            "mdi:heat-wave",
            "starlinkalert",
        )
    )

    async_add_entities(sensors)


class StarlinkBinarySensor(BinarySensorEntity):
    """Defines a Starlink Binary sensor."""

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
    def should_poll(self) -> bool:
        """No need to poll. Coordinator notifies entity of updates."""
        return False

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

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

        device_name = "Starlink Alerts"
        device_model = "Alerts"

        return {
            ATTR_IDENTIFIERS: {(DOMAIN, self._device_identifier)},
            ATTR_NAME: device_name,
            ATTR_MANUFACTURER: "Starlink",
            ATTR_MODEL: device_model,
        }

    @property
    def is_on(self) -> bool:
        """Return the state."""
        starlink_data = self.coordinator.data

        if self._kind == "starlink_currently_obstructed":
            return starlink_data["currently_obstructed"] == 'True'
        elif self._kind == "starlink_alert_motors_stuck":
            return starlink_data["alert_motors_stuck"] == 'True'
        elif self._kind == "starlink_alert_thermal_throttle":
            return starlink_data["alert_thermal_throttle"] == 'True'
        elif self._kind == "starlink_alert_thermal_shutdown":
            return starlink_data["alert_thermal_shutdown"] == 'True'
        elif self._kind == "starlink_alert_mast_not_near_vertical":
            return starlink_data["alert_mast_not_near_vertical"] == 'True'
        elif self._kind == "starlink_alert_unexpected_location":
            return starlink_data["alert_unexpected_location"] == 'True'
        elif self._kind == "starlink_alert_slow_ethernet_speeds":
            return starlink_data["alert_slow_ethernet_speeds"] == 'True'
        elif self._kind == "starlink_alert_roaming":
            return starlink_data["alert_roaming"] == 'True'
        elif self._kind == "starlink_alert_install_pending":
            return starlink_data["alert_install_pending"] == 'True'
        elif self._kind == "starlink_alert_is_heating":
            return starlink_data["alert_is_heating"] == 'True'

    async def async_update(self):
        """Update Starlink Binary Sensor Entity."""
        await self.coordinator.async_request_refresh()

    async def async_added_to_hass(self):
        """Subscribe to updates."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
