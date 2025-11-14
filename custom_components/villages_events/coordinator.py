"""Data update coordinator for The Villages Events integration.

This module implements the data update coordinator that manages fetching
event data from The Villages calendar and distributing it to sensor entities.

The coordinator:
    - Fetches data from python-villages-events library at configured intervals
    - Structures data by venue and time period (today/tomorrow)
    - Matches events against favorite performers
    - Implements error handling with exponential backoff
    - Maintains last known state during failures

The coordinator follows Home Assistant's DataUpdateCoordinator pattern for
efficient data management and automatic entity updates.
"""
from __future__ import annotations

from datetime import datetime, timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import (
    CONF_FAVORITE_PERFORMERS,
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
    MAX_CONSECUTIVE_FAILURES,
    PERIOD_TODAY,
    PERIOD_TOMORROW,
    RETRY_BACKOFF_MINUTES,
)

_LOGGER = logging.getLogger(__name__)


class VillagesEventsCoordinator(DataUpdateCoordinator):
    """Coordinator for fetching Villages Events data.
    
    This coordinator manages data updates from the python-villages-events
    library and distributes the data to sensor entities. It handles data
    fetching, error recovery, and favorite performer matching.
    
    The coordinator automatically updates at the configured interval and
    implements exponential backoff on failures to avoid overwhelming the
    API during outages.
    
    Attributes:
        config_entry: The config entry for this integration
        favorite_performers: List of performer names to track (lowercase)
        consecutive_failures: Counter for tracking consecutive update failures
    
    Example:
        ```python
        coordinator = VillagesEventsCoordinator(hass, config_entry)
        await coordinator.async_config_entry_first_refresh()
        
        # Access data
        venues = coordinator.data["venues"]
        favorite_today = coordinator.data["favorite_today"]
        ```
    """

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the coordinator.
        
        Args:
            hass: Home Assistant instance
            config_entry: Config entry containing user configuration
        """
        self.config_entry = config_entry
        
        # Extract configuration
        update_interval_minutes = config_entry.data.get(
            CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
        )
        self.favorite_performers = config_entry.data.get(
            CONF_FAVORITE_PERFORMERS, []
        )
        
        # Convert favorite performers to lowercase for case-insensitive matching
        if isinstance(self.favorite_performers, str):
            self.favorite_performers = [
                p.strip().lower() 
                for p in self.favorite_performers.split(",") 
                if p.strip()
            ]
        elif isinstance(self.favorite_performers, list):
            self.favorite_performers = [p.lower() for p in self.favorite_performers]
        
        # Track consecutive failures for error handling
        self.consecutive_failures = 0
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=update_interval_minutes),
        )


    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from The Villages calendar.
        
        Returns:
            Dictionary containing venue events and favorite performer matches.
            Structure:
            {
                "venues": {
                    "venue_name": {
                        "today": [event_dict, ...],
                        "tomorrow": [event_dict, ...]
                    }
                },
                "favorite_today": bool,
                "favorite_tomorrow": bool,
                "favorite_events": {
                    "today": [event_dict, ...],
                    "tomorrow": [event_dict, ...]
                }
            }
            
        Raises:
            UpdateFailed: When data fetch fails after retries.
        """
        try:
            # Import here to avoid issues if library not installed
            from villages_events import VillagesEvents
            
            # Calculate today and tomorrow based on HA timezone
            now = dt_util.now()
            today = now.date()
            tomorrow = (now + timedelta(days=1)).date()
            
            _LOGGER.debug(
                "Fetching events for %s (today) and %s (tomorrow)",
                today,
                tomorrow,
            )
            
            # Fetch events using executor (library is synchronous)
            client = VillagesEvents()
            events = await self.hass.async_add_executor_job(
                client.get_events,
                today,
                tomorrow,
            )
            
            # Structure data by venue and period
            venues_data = {}
            
            for event in events:
                venue_name = event.get("venue", "Unknown Venue")
                event_date = event.get("date")
                
                # Determine if event is today or tomorrow
                if event_date == today:
                    period = PERIOD_TODAY
                elif event_date == tomorrow:
                    period = PERIOD_TOMORROW
                else:
                    # Skip events outside our date range
                    continue
                
                # Initialize venue structure if needed
                if venue_name not in venues_data:
                    venues_data[venue_name] = {
                        PERIOD_TODAY: [],
                        PERIOD_TOMORROW: [],
                    }
                
                # Create event dictionary
                event_dict = {
                    "performer": event.get("performer", "Unknown"),
                    "start_time": event.get("start_time"),
                    "end_time": event.get("end_time"),
                    "event_type": event.get("event_type", "Event"),
                }
                
                # Add to appropriate period
                venues_data[venue_name][period].append(event_dict)
            
            # Build result dictionary
            result = {
                "venues": venues_data,
            }
            
            # Add favorite performer matching if configured
            result.update(self._match_favorite_performers(venues_data))
            
            # Reset consecutive failures on success
            if self.consecutive_failures > 0:
                _LOGGER.info(
                    "Successfully recovered from %d consecutive failures",
                    self.consecutive_failures,
                )
                self.consecutive_failures = 0
                
                # Restore normal update interval
                update_interval_minutes = self.config_entry.data.get(
                    CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
                )
                self.update_interval = timedelta(minutes=update_interval_minutes)
                _LOGGER.info(
                    "Restored normal update interval to %d minutes",
                    update_interval_minutes,
                )
            else:
                self.consecutive_failures = 0
            
            _LOGGER.debug(
                "Successfully fetched events for %d venues",
                len(venues_data),
            )
            
            return result
            
        except ImportError as err:
            _LOGGER.error(
                "python-villages-events library not installed: %s",
                err,
            )
            raise UpdateFailed(
                "python-villages-events library not available"
            ) from err
            
        except (ConnectionError, TimeoutError) as err:
            self.consecutive_failures += 1
            _LOGGER.warning(
                "Network error fetching Villages Events data "
                "(failure %d/%d): %s. Will retry.",
                self.consecutive_failures,
                MAX_CONSECUTIVE_FAILURES,
                err,
            )
            
            # Adjust update interval for exponential backoff
            if self.consecutive_failures <= len(RETRY_BACKOFF_MINUTES):
                backoff_minutes = RETRY_BACKOFF_MINUTES[self.consecutive_failures - 1]
                self.update_interval = timedelta(minutes=backoff_minutes)
                _LOGGER.info(
                    "Adjusting update interval to %d minutes for retry",
                    backoff_minutes,
                )
            
            # Mark unavailable after max failures
            if self.consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                _LOGGER.error(
                    "Maximum consecutive failures reached. "
                    "Entities will be marked unavailable."
                )
            
            raise UpdateFailed(f"Network error: {err}") from err
            
        except Exception as err:
            self.consecutive_failures += 1
            _LOGGER.error(
                "Unexpected error fetching Villages Events data "
                "(failure %d/%d): %s",
                self.consecutive_failures,
                MAX_CONSECUTIVE_FAILURES,
                err,
                exc_info=True,
            )
            
            # Mark unavailable after max failures
            if self.consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                _LOGGER.error(
                    "Maximum consecutive failures reached. "
                    "Entities will be marked unavailable."
                )
            
            raise UpdateFailed(f"Error fetching data: {err}") from err


    def _match_favorite_performers(
        self, venues_data: dict[str, dict[str, list[dict[str, Any]]]]
    ) -> dict[str, Any]:
        """Match events against favorite performers list.
        
        Performs case-insensitive substring matching to find events where
        any configured favorite performer name appears in the event's
        performer field.
        
        Args:
            venues_data: Dictionary of venues with their events, structured as:
                {
                    "venue_name": {
                        "today": [event_dict, ...],
                        "tomorrow": [event_dict, ...]
                    }
                }
            
        Returns:
            Dictionary with favorite performer matching results:
            {
                "favorite_today": bool,  # True if any favorites today
                "favorite_tomorrow": bool,  # True if any favorites tomorrow
                "favorite_events": {
                    "today": [event_dict, ...],  # Events with venue added
                    "tomorrow": [event_dict, ...]
                }
            }
        
        Example:
            ```python
            venues = {
                "Spanish Springs": {
                    "today": [{"performer": "The Beatles"}]
                }
            }
            result = coordinator._match_favorite_performers(venues)
            # result["favorite_today"] == True if "beatles" in favorites
            ```
        """
        favorite_events_today = []
        favorite_events_tomorrow = []
        
        # If no favorite performers configured, return empty results
        if not self.favorite_performers:
            return {
                "favorite_today": False,
                "favorite_tomorrow": False,
                "favorite_events": {
                    PERIOD_TODAY: [],
                    PERIOD_TOMORROW: [],
                },
            }
        
        # Iterate through all venues and events
        for venue_name, periods in venues_data.items():
            # Check today's events
            for event in periods.get(PERIOD_TODAY, []):
                performer = event.get("performer", "").lower()
                # Check if performer matches any favorite (case-insensitive)
                if any(fav in performer for fav in self.favorite_performers):
                    event_with_venue = event.copy()
                    event_with_venue["venue"] = venue_name
                    favorite_events_today.append(event_with_venue)
            
            # Check tomorrow's events
            for event in periods.get(PERIOD_TOMORROW, []):
                performer = event.get("performer", "").lower()
                # Check if performer matches any favorite (case-insensitive)
                if any(fav in performer for fav in self.favorite_performers):
                    event_with_venue = event.copy()
                    event_with_venue["venue"] = venue_name
                    favorite_events_tomorrow.append(event_with_venue)
        
        _LOGGER.debug(
            "Found %d favorite events today, %d tomorrow",
            len(favorite_events_today),
            len(favorite_events_tomorrow),
        )
        
        return {
            "favorite_today": len(favorite_events_today) > 0,
            "favorite_tomorrow": len(favorite_events_tomorrow) > 0,
            "favorite_events": {
                PERIOD_TODAY: favorite_events_today,
                PERIOD_TOMORROW: favorite_events_tomorrow,
            },
        }


    @property
    def is_unavailable(self) -> bool:
        """Check if coordinator should mark entities as unavailable.
        
        Entities should be marked unavailable after MAX_CONSECUTIVE_FAILURES
        to indicate to users that data is stale and updates are failing.
        
        Returns:
            True if consecutive failures exceed threshold, False otherwise.
        
        Example:
            ```python
            if coordinator.is_unavailable:
                # Entity should return None for state
                return None
            ```
        """
        return self.consecutive_failures >= MAX_CONSECUTIVE_FAILURES
