"""Binary sensor platform for The Villages Events integration.

This module implements binary sensor entities that track whether favorite
performers have events scheduled. These sensors enable automations and
notifications based on favorite performer appearances.

Two binary sensors are created:
    - binary_sensor.villages_events_favorite_today
    - binary_sensor.villages_events_favorite_tomorrow

Sensors are "on" when at least one favorite performer is scheduled, and "off"
when no favorites are scheduled. Matching event details are available in
entity attributes.
"""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import (
    ATTR_COUNT,
    ATTR_FAVORITE_PERFORMERS,
    ATTR_MATCHING_EVENTS,
    DOMAIN,
    ENTITY_ID_FAVORITE_TODAY,
    ENTITY_ID_FAVORITE_TOMORROW,
    PERIOD_TODAY,
    PERIOD_TOMORROW,
)
from .coordinator import VillagesEventsCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Villages Events binary sensor entities.
    
    Args:
        hass: Home Assistant instance
        config_entry: Config entry for this integration
        async_add_entities: Callback to add entities to Home Assistant
    """
    # Retrieve coordinator from hass.data
    coordinator: VillagesEventsCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    entities = []
    
    # Create binary sensor for favorite performers today
    entities.append(
        VillagesFavoritePerformerSensor(
            coordinator=coordinator,
            period=PERIOD_TODAY,
        )
    )
    
    # Create binary sensor for favorite performers tomorrow
    entities.append(
        VillagesFavoritePerformerSensor(
            coordinator=coordinator,
            period=PERIOD_TOMORROW,
        )
    )
    
    # Add entities to Home Assistant
    async_add_entities(entities)
    
    _LOGGER.info(
        "Set up %d Villages Events binary sensor entities",
        len(entities),
    )


class VillagesFavoritePerformerSensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor for tracking favorite performer appearances.
    
    This sensor indicates whether any favorite performers have events
    scheduled for a specific period (today or tomorrow). The sensor is
    "on" when at least one favorite performer is scheduled, and "off"
    when no favorites are scheduled.
    
    This enables automations like sending notifications when a favorite
    performer is scheduled to play.
    
    Entity IDs:
        - binary_sensor.villages_events_favorite_today
        - binary_sensor.villages_events_favorite_tomorrow
    
    Attributes:
        period: Time period ("today" or "tomorrow")
    
    Example:
        ```python
        sensor = VillagesFavoritePerformerSensor(
            coordinator=coordinator,
            period="today"
        )
        # sensor.is_on returns True if favorites are scheduled today
        # sensor.extra_state_attributes includes matching event details
        ```
    """

    def __init__(
        self,
        coordinator: VillagesEventsCoordinator,
        period: str,
    ) -> None:
        """Initialize the binary sensor.
        
        Args:
            coordinator: Data update coordinator
            period: Time period (today or tomorrow)
        """
        super().__init__(coordinator)
        
        self.period = period
        
        # Set entity ID based on period
        if period == PERIOD_TODAY:
            self.entity_id = f"binary_sensor.{ENTITY_ID_FAVORITE_TODAY}"
            self._attr_unique_id = f"{DOMAIN}_favorite_today"
            self._attr_name = "Villages Events Favorite Today"
        else:
            self.entity_id = f"binary_sensor.{ENTITY_ID_FAVORITE_TOMORROW}"
            self._attr_unique_id = f"{DOMAIN}_favorite_tomorrow"
            self._attr_name = "Villages Events Favorite Tomorrow"
        
        # Set device class to presence
        self._attr_device_class = BinarySensorDeviceClass.PRESENCE
        
        # Set icon
        self._attr_icon = "mdi:star-circle"


    @property
    def is_on(self) -> bool | None:
        """Return true if favorite performer has events scheduled.
        
        Returns:
            True if favorite performers are scheduled, False otherwise,
            None if unavailable
        """
        # Check if coordinator is unavailable
        if self.coordinator.is_unavailable:
            return None
        
        # Get favorite performer data from coordinator
        if not self.coordinator.data:
            return False
        
        # Check the appropriate period flag
        if self.period == PERIOD_TODAY:
            return self.coordinator.data.get("favorite_today", False)
        else:
            return self.coordinator.data.get("favorite_tomorrow", False)


    @property
    def available(self) -> bool:
        """Return if entity is available.
        
        Returns:
            False if coordinator has exceeded max failures, True otherwise
        """
        return not self.coordinator.is_unavailable


    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes.
        
        Returns:
            Dictionary containing favorite_performers list, matching_events,
            and count of matching events
        """
        attributes = {
            ATTR_FAVORITE_PERFORMERS: [],
            ATTR_MATCHING_EVENTS: [],
            ATTR_COUNT: 0,
        }
        
        # Return empty attributes if coordinator is unavailable
        if self.coordinator.is_unavailable:
            return attributes
        
        # Add favorite performers list from configuration
        attributes[ATTR_FAVORITE_PERFORMERS] = self.coordinator.favorite_performers
        
        # Get matching events from coordinator data
        if not self.coordinator.data or "favorite_events" not in self.coordinator.data:
            return attributes
        
        favorite_events = self.coordinator.data["favorite_events"]
        matching_events = favorite_events.get(self.period, [])
        
        # Format matching events for attributes
        formatted_events = []
        for event in matching_events:
            formatted_event = {
                "performer": event.get("performer", "Unknown"),
                "venue": event.get("venue", "Unknown Venue"),
            }
            
            # Format start_time if available
            start_time = event.get("start_time")
            if start_time:
                if isinstance(start_time, datetime):
                    formatted_event["start_time"] = start_time.isoformat()
                else:
                    formatted_event["start_time"] = str(start_time)
            else:
                formatted_event["start_time"] = None
            
            # Format end_time if available
            end_time = event.get("end_time")
            if end_time:
                if isinstance(end_time, datetime):
                    formatted_event["end_time"] = end_time.isoformat()
                else:
                    formatted_event["end_time"] = str(end_time)
            else:
                formatted_event["end_time"] = None
            
            formatted_events.append(formatted_event)
        
        attributes[ATTR_MATCHING_EVENTS] = formatted_events
        attributes[ATTR_COUNT] = len(formatted_events)
        
        return attributes
