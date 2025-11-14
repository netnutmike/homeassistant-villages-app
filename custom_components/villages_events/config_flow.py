"""Config flow for The Villages Events integration.

This module implements the configuration flow for setting up and modifying
The Villages Events integration through the Home Assistant UI.

The config flow handles:
    - Initial integration setup with validation
    - Options flow for reconfiguring existing instances
    - Input validation for update intervals and favorite performers
    - Error handling and user feedback

Configuration is stored in Home Assistant's config entry system and can be
modified without removing and re-adding the integration.
"""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_FAVORITE_PERFORMERS,
    CONF_UPDATE_INTERVAL,
    DEFAULT_FAVORITE_PERFORMERS,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
    MAX_UPDATE_INTERVAL,
    MIN_UPDATE_INTERVAL,
)


class VillagesEventsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for The Villages Events.
    
    This class manages the initial configuration of the integration through
    the Home Assistant UI. It validates user inputs and creates the config
    entry that stores the integration settings.
    
    Configuration options:
        - update_interval: How often to fetch data (15-1440 minutes)
        - favorite_performers: Comma-separated list of performer names
    
    Example flow:
        1. User adds integration through UI
        2. async_step_user() displays configuration form
        3. User enters update interval and favorite performers
        4. Inputs are validated
        5. Config entry is created on success
    """

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial configuration step.
        
        Displays a form for users to configure the integration. Validates
        the update interval and parses the favorite performers list.
        
        Args:
            user_input: Dictionary containing user-provided configuration,
                or None if form should be displayed
        
        Returns:
            FlowResult indicating next step (show form or create entry)
        
        Example:
            ```python
            # User input example:
            {
                "update_interval": 60,
                "favorite_performers": "Artist 1, Artist 2, Artist 3"
            }
            ```
        """
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate update interval
            update_interval = user_input.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
            if not isinstance(update_interval, int) or not (
                MIN_UPDATE_INTERVAL <= update_interval <= MAX_UPDATE_INTERVAL
            ):
                errors[CONF_UPDATE_INTERVAL] = "invalid_update_interval"

            # Validate and parse favorite performers
            favorite_performers_str = user_input.get(CONF_FAVORITE_PERFORMERS, "")
            favorite_performers = []
            
            if favorite_performers_str:
                # Split by comma and strip whitespace
                favorite_performers = [
                    performer.strip()
                    for performer in favorite_performers_str.split(",")
                    if performer.strip()
                ]

            # If no errors, create the config entry
            if not errors:
                return self.async_create_entry(
                    title="The Villages Events",
                    data={
                        CONF_UPDATE_INTERVAL: update_interval,
                        CONF_FAVORITE_PERFORMERS: favorite_performers,
                    },
                )

        # Show the configuration form
        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_UPDATE_INTERVAL,
                    default=DEFAULT_UPDATE_INTERVAL,
                ): int,
                vol.Optional(
                    CONF_FAVORITE_PERFORMERS,
                    default="",
                ): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> VillagesEventsOptionsFlow:
        """Get the options flow for this handler."""
        return VillagesEventsOptionsFlow(config_entry)


class VillagesEventsOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for The Villages Events.
    
    This class manages reconfiguration of an existing integration instance.
    Users can update the update interval and favorite performers list
    without removing and re-adding the integration.
    
    Changes trigger a reload of the integration to apply new settings.
    
    Example:
        ```python
        # User opens integration options
        # async_step_init() displays current settings
        # User modifies settings
        # Integration reloads with new configuration
        ```
    """

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow.
        
        Args:
            config_entry: The existing config entry to modify
        """
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options for an existing config entry.
        
        Displays a form pre-filled with current settings. Validates
        changes and updates the config entry on success.
        
        Args:
            user_input: Dictionary containing updated configuration,
                or None if form should be displayed with current values
        
        Returns:
            FlowResult indicating next step (show form or update entry)
        """
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate update interval
            update_interval = user_input.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
            if not isinstance(update_interval, int) or not (
                MIN_UPDATE_INTERVAL <= update_interval <= MAX_UPDATE_INTERVAL
            ):
                errors[CONF_UPDATE_INTERVAL] = "invalid_update_interval"

            # Validate and parse favorite performers
            favorite_performers_str = user_input.get(CONF_FAVORITE_PERFORMERS, "")
            favorite_performers = []
            
            if favorite_performers_str:
                # Split by comma and strip whitespace
                favorite_performers = [
                    performer.strip()
                    for performer in favorite_performers_str.split(",")
                    if performer.strip()
                ]

            # If no errors, update the config entry
            if not errors:
                return self.async_create_entry(
                    title="",
                    data={
                        CONF_UPDATE_INTERVAL: update_interval,
                        CONF_FAVORITE_PERFORMERS: favorite_performers,
                    },
                )

        # Get current values from config entry
        current_update_interval = self.config_entry.data.get(
            CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
        )
        current_favorite_performers = self.config_entry.data.get(
            CONF_FAVORITE_PERFORMERS, DEFAULT_FAVORITE_PERFORMERS
        )
        
        # Convert list to comma-separated string for display
        favorite_performers_str = ", ".join(current_favorite_performers)

        # Show the options form
        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_UPDATE_INTERVAL,
                    default=current_update_interval,
                ): int,
                vol.Optional(
                    CONF_FAVORITE_PERFORMERS,
                    default=favorite_performers_str,
                ): str,
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
            errors=errors,
        )
