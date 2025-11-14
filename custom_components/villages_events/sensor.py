"""Sensor platform for The Villages Events integration.

This module implements sensor entities that display event information for
each venue at The Villages. Sensors are created dynamically based on the
venues returned by the python-villages-events library.

Each venue gets two sensors:
    - One for today's events
    - One for tomorrow's events

Sensor state is the count of events, and detailed event information
(performer, times, event type) is available in entity attributes.

Entity naming follows the pattern: sensor.villages_events_{venue_slug}_{period}
"""
from __future__ import annotations

from datetime import datetime
import logging
import re
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import (
    ATTR_EVENTS,
    ATTR_LAST_UPDATED,
    ATTR_PERIOD,
    ATTR_VENUE,
    DOMAIN,
    PERIOD_TODAY,
    PERIOD_TOMORROW,
    UNIT_EVENTS,
)
from .coordinator import VillagesEventsCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Villages Events sensor entities.
    
    Args:
        hass: Home Assistant instance
        config_entry: Config entry for this integration
        async_add_entities: Callback to add entities to Home Assistant
    """
    # Retrieve coordinator from hass.data
    coordinator: VillagesEventsCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    entities = []
    
    # Create sensor entities for each venue and period
    if coordinator.data and "venues" in coordinator.data:
        venues_data = coordinator.data["venues"]
        
        for venue_name in venues_data.keys():
            # Create sensor for today's events
            entities.append(
                VillagesEventSensor(
                    coordinator=coordinator,
                    venue_name=venue_name,
                    period=PERIOD_TODAY,
                )
            )
            
            # Create sensor for tomorrow's events
            entities.append(
                VillagesEventSensor(
                    coordinator=coordinator,
                    venue_name=venue_name,
                    period=PERIOD_TOMORROW,
                )
            )
    
    # Add entities to Home Assistant
    async_add_entities(entities)
    
    _LOGGER.info(
        "Set up %d Villages Events sensor entities",
        len(entities),
    )



class VillagesEventSensor(CoordinatorEntity, SensorEntity):
    """Sensor entity for venue events at The Villages.
    
    This sensor displays the number of events scheduled at a specific venue
    for a specific period (today or tomorrow). The sensor state is the count
    of events, and detailed event information is available in attributes.
    
    Entity IDs follow the pattern: sensor.villages_events_{venue_slug}_{period}
    For example: sensor.villages_events_spanish_springs_today
    
    Attributes:
        venue_name: Name of the venue (e.g., "Spanish Springs Town Square")
        period: Time period ("today" or "tomorrow")
    
    Example:
        ```python
        sensor = VillagesEventSensor(
            coordinator=coordinator,
            venue_name="Spanish Springs Town Square",
            period="today"
        )
        # sensor.state returns number of events (e.g., 3)
        # sensor.extra_state_attributes returns event details
        ```
    """

    def __init__(
        self,
        coordinator: VillagesEventsCoordinator,
        venue_name: str,
        period: str,
    ) -> None:
        """Initialize the sensor.
        
        Args:
            coordinator: Data update coordinator
            venue_name: Name of the venue
            period: Time period (today or tomorrow)
        """
        super().__init__(coordinator)
        
        self.venue_name = venue_name
        self.period = period
        
        # Create venue slug for entity ID
        self._venue_slug = self._create_slug(venue_name)
        
        # Set entity ID
        self.entity_id = f"sensor.villages_events_{self._venue_slug}_{period}"
        
        # Set unique ID
        self._attr_unique_id = f"{DOMAIN}_{self._venue_slug}_{period}"
        
        # Set entity name
        self._attr_name = f"Villages Events {venue_name} {period.capitalize()}"
        
        # Set unit of measurement
        self._attr_native_unit_of_measurement = UNIT_EVENTS
        
        # Set icon
        self._attr_icon = "mdi:calendar-music"


    @staticmethod
    def _create_slug(name: str) -> str:
        """Create a URL-safe slug from venue name.
        
        Converts venue names to lowercase, replaces spaces and special
        characters with underscores, and removes leading/trailing underscores.
        
        Args:
            name: Venue name to convert (e.g., "Spanish Springs Town Square")
            
        Returns:
            URL-safe slug in lowercase with underscores (e.g., "spanish_springs_town_square")
        
        Example:
            ```python
            slug = VillagesEventSensor._create_slug("Lake Sumter Landing")
            # Returns: "lake_sumter_landing"
            
            slug = VillagesEventSensor._create_slug("Brownwood Paddock Square")
            # Returns: "brownwood_paddock_square"
            ```
        """
        # Convert to lowercase
        slug = name.lower()
        # Replace spaces and special characters with underscores
        slug = re.sub(r'[^a-z0-9]+', '_', slug)
        # Remove leading/trailing underscores
        slug = slug.strip('_')
        return slug


    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor.
        
        Returns:
            Number of events scheduled, or None if unavailable
        """
        # Check if coordinator is unavailable
        if self.coordinator.is_unavailable:
            return None
        
        # Get venue data from coordinator
        if not self.coordinator.data or "venues" not in self.coordinator.data:
            return 0
        
        venues_data = self.coordinator.data["venues"]
        
        # Get events for this venue and period
        if self.venue_name not in venues_data:
            return 0
        
        venue_data = venues_data[self.venue_name]
        events = venue_data.get(self.period, [])
        
        return len(events)


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
            Dictionary containing venue, period, events list, and last_updated
        """
        attributes = {
            ATTR_VENUE: self.venue_name,
            ATTR_PERIOD: self.period,
            ATTR_EVENTS: [],
            ATTR_LAST_UPDATED: None,
        }
        
        # Return empty attributes if coordinator is unavailable
        if self.coordinator.is_unavailable:
            return attributes
        
        # Get venue data from coordinator
        if not self.coordinator.data or "venues" not in self.coordinator.data:
            attributes[ATTR_LAST_UPDATED] = dt_util.now().isoformat()
            return attributes
        
        venues_data = self.coordinator.data["venues"]
        
        # Get events for this venue and period
        if self.venue_name in venues_data:
            venue_data = venues_data[self.venue_name]
            events = venue_data.get(self.period, [])
            
            # Format events for attributes
            formatted_events = []
            for event in events:
                formatted_event = {
                    "performer": event.get("performer", "Unknown"),
                    "event_type": event.get("event_type", "Event"),
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
            
            attributes[ATTR_EVENTS] = formatted_events
        
        # Add last updated timestamp
        attributes[ATTR_LAST_UPDATED] = dt_util.now().isoformat()
        
        return attributes
