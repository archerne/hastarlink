"""Definition and setup of the Starlink Binary Sensors for Home Assistant."""

import logging
import time
import datetime

from homeassistant.util.dt import as_local, utc_from_timestamp
from homeassistant.components.sensor import ENTITY_ID_FORMAT, DEVICE_CLASS_TIMESTAMP
from homeassistant.const import DATA_RATE_MEGABITS_PER_SECOND, PERCENTAGE, TIME_MILLISECONDS, TIME_SECONDS, ATTR_NAME, CONF_LATITUDE, CONF_LONGITUDE, CONF_ELEVATION
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from . import StarlinkUpdateCoordinator

from .const import ATTR_IDENTIFIERS, ATTR_MANUFACTURER, ATTR_MODEL, DOMAIN, COORDINATOR

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platforms."""

    coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]
    sensors = []

    sensors.append(
        StarlinkSensor(
            coordinator,
            "Software Version",
            "starlink_software_version",
            "mdi:information-outline",
            "starlinkstats",
        )
    )

    sensors.append(
        StarlinkSensor(
            coordinator,
            "State",
            "starlink_state",
            "mdi:information-outline",
            "starlinkstats",
        )
    )

    sensors.append(
        StarlinkSensor(
            coordinator,
            "Uptime",
            "starlink_uptime",
            "mdi:timer-outline",
            "starlinkstats",
        )
    )

    sensors.append(
        StarlinkSensor(
            coordinator,
            "Ping Drop Rate",
            "starlink_pop_ping_drop_rate",
            "mdi:information-outline",
            "starlinkstats",
        )
    )

    sensors.append(
        StarlinkSensor(
            coordinator,
            "Downlink Throughput",
            "starlink_downlink_throughput_mbps",
            "mdi:information-outline",
            "starlinkstats",
        )
    )

    sensors.append(
        StarlinkSensor(
            coordinator,
            "Uplink Throughput",
            "starlink_uplink_throughput_mbps",
            "mdi:information-outline",
            "starlinkstats",
        )
    )

    sensors.append(
        StarlinkSensor(
            coordinator,
            "Ping Latency",
            "starlink_pop_ping_latency_ms",
            "mdi:information-outline",
            "starlinkstats",
        )
    )

    sensors.append(
        StarlinkSensor(
            coordinator,
            "Dish Latitude",
            "starlink_latitude",
            "mdi:information-outline",
            "starlinkstats",
        )
    )

    sensors.append(
        StarlinkSensor(
            coordinator,
            "Dish Longitude",
            "starlink_longitude",
            "mdi:information-outline",
            "starlinkstats",
        )
    )

    sensors.append(
        StarlinkSensor(
            coordinator,
            "Dish Altitude",
            "starlink_altitude",
            "mdi:information-outline",
            "starlinkstats",
        )
    )
    async_add_entities(sensors)


class StarlinkSensor(CoordinatorEntity):
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

        super().__init__(coordinator=coordinator)

        self._name = name
        self._unique_id = f"starlink_{entity_id}"
        self._state = None
        self._icon = icon
        self._kind = entity_id
        self._device_identifier = device_identifier
        self._unit_of_measure = None
        self.attrs = {}

        if self._kind == "starlink_downlink_throughput_mbps":
            self._unit_of_measure = DATA_RATE_MEGABITS_PER_SECOND

        elif self._kind == "starlink_uplink_throughput_mbps":
            self._unit_of_measure = DATA_RATE_MEGABITS_PER_SECOND

        elif self._kind == "starlink_pop_ping_drop_rate":
            self._unit_of_measure = PERCENTAGE

        elif self._kind == "starlink_pop_ping_latency_ms":
            self._unit_of_measure = TIME_MILLISECONDS

        elif self._kind == "starlink_uptime":
            self._unit_of_measure = TIME_SECONDS

        elif self._kind == "starlink_latitude":
            self._unit_of_measure = CONF_LATITUDE

        elif self._kind == "starlink_longitude":
            self._unit_of_measure = CONF_LONGITUDE

        elif self._kind == "starlink_altitude":
            self._unit_of_measure = CONF_ELEVATION

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
    def unit_of_measurement(self):
        """Return the unit of measurement for this entity."""
        return self._unit_of_measure

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

    @property
    def state(self):
        """Return the state."""
        coordinator_data = self.coordinator.data

        if self._kind == "starlink_software_version":
            self._state = coordinator_data["software_version"]

        elif self._kind == "starlink_state":
            self._state = coordinator_data["state"]

        elif self._kind == "starlink_downlink_throughput_mbps":
            self._state = round(
                (float(coordinator_data["downlink_throughput_bps"])/1000000), 2)
            self._unit_of_measure = DATA_RATE_MEGABITS_PER_SECOND

        elif self._kind == "starlink_uplink_throughput_mbps":
            self._state = round(
                (float(coordinator_data["uplink_throughput_bps"])/1000000), 2)
            self._unit_of_measure = DATA_RATE_MEGABITS_PER_SECOND
        elif self._kind == "starlink_pop_ping_drop_rate":
            self._state = round(
                (float(coordinator_data["pop_ping_drop_rate"])*100), 2)
            self._unit_of_measure = PERCENTAGE
        elif self._kind == "starlink_pop_ping_latency_ms":
            self._state = round(
                float(coordinator_data["pop_ping_latency_ms"]), 2)
            self._unit_of_measure = TIME_MILLISECONDS
        elif self._kind == "starlink_uptime":
            self._state = int(coordinator_data["uptime"])
            self._unit_of_measure = TIME_SECONDS
        elif self._kind == "starlink_latitude":
            self._state = round(
                float(coordinator_data["latitude"]), 4)
            self._unit_of_measure = CONF_LATITUDE
        elif self._kind == "starlink_longitude":
            self._state = round(
                float(coordinator_data["longitude"]), 4)
            self._unit_of_measure = CONF_LONGITUDE
        elif self._kind == "starlink_altitude":
            self._state = round(
                float(coordinator_data["altitude"]), 4)
            self._unit_of_measure = CONF_ELEVATION

        return self._state

    async def async_update(self):
        """Update Starlink Binary Sensor Entity."""
        await self.coordinator.async_request_refresh()
        _LOGGER.debug("Updating state of the sensors.")

    async def async_added_to_hass(self):
        """Subscribe to updates."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
