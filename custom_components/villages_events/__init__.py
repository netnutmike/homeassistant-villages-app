"""The Villages Events integration.

This integration provides Home Assistant with access to entertainment event
information from The Villages, Florida. It creates sensor entities for each
venue showing today's and tomorrow's events, along with binary sensors for
tracking favorite performers.

The integration uses a coordinator-based architecture to efficiently fetch
and distribute data to multiple entities. Data is fetched from the
python-villages-events library at a configurable interval.

Main components:
    - VillagesEventsCoordinator: Manages data fetching and updates
    - Sensor entities: Display event counts and details per venue
    - Binary sensor entities: Track favorite performer appearances

Example:
    ```python
    # Integration is set up through Home Assistant UI
    # Entities are automatically created:
    # - sensor.villages_events_spanish_springs_today
    # - sensor.villages_events_spanish_springs_tomorrow
    # - binary_sensor.villages_events_favorite_today
    # - binary_sensor.villages_events_favorite_tomorrow
    ```
"""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .coordinator import VillagesEventsCoordinator

_LOGGER = logging.getLogger(__name__)

# Platforms supported by this integration
PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up The Villages Events from a config entry.
    
    Args:
        hass: Home Assistant instance
        entry: Config entry containing user configuration
        
    Returns:
        True if setup was successful, False otherwise
        
    Raises:
        ConfigEntryNotReady: If initial data fetch fails
    """
    _LOGGER.debug("Setting up The Villages Events integration")
    
    # Create coordinator instance
    coordinator = VillagesEventsCoordinator(hass, entry)
    
    # Perform initial data fetch
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        _LOGGER.error("Failed to fetch initial data: %s", err)
        raise ConfigEntryNotReady(f"Failed to fetch initial data: {err}") from err
    
    # Store coordinator in hass.data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    _LOGGER.info(
        "Successfully initialized The Villages Events coordinator with "
        "%d venues",
        len(coordinator.data.get("venues", {})),
    )
    
    # Forward setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry.
    
    Args:
        hass: Home Assistant instance
        entry: Config entry to unload
        
    Returns:
        True if unload was successful, False otherwise
    """
    _LOGGER.debug("Unloading The Villages Events integration")
    
    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        # Remove coordinator from hass.data
        coordinator = hass.data[DOMAIN].pop(entry.entry_id)
        
        # Clean up coordinator resources if needed
        # The coordinator will automatically stop updates when no longer referenced
        _LOGGER.info("Successfully unloaded The Villages Events integration")
    else:
        _LOGGER.error("Failed to unload The Villages Events platforms")
    
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry.
    
    Args:
        hass: Home Assistant instance
        entry: Config entry to reload
    """
    _LOGGER.debug("Reloading The Villages Events integration")
    
    # Unload the entry
    await async_unload_entry(hass, entry)
    
    # Set up the entry again with updated configuration
    await async_setup_entry(hass, entry)
