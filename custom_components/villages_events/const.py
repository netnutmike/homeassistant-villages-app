"""Constants for The Villages Events integration.

This module defines all constants used throughout the integration including
configuration keys, default values, entity naming patterns, and attribute keys.
"""

# Integration domain - unique identifier for this integration
DOMAIN = "villages_events"

# Platforms supported by this integration
SENSOR = "sensor"
BINARY_SENSOR = "binary_sensor"

# Configuration keys used in config entries
CONF_UPDATE_INTERVAL = "update_interval"  # How often to fetch data (minutes)
CONF_FAVORITE_PERFORMERS = "favorite_performers"  # List of favorite performer names

# Default configuration values
DEFAULT_UPDATE_INTERVAL = 60  # Default update interval in minutes
DEFAULT_FAVORITE_PERFORMERS = []  # Empty list means no favorites configured

# Update interval constraints to prevent excessive API calls or stale data
MIN_UPDATE_INTERVAL = 15  # Minimum update interval in minutes
MAX_UPDATE_INTERVAL = 1440  # Maximum update interval in minutes (24 hours)

# Retry configuration for handling transient failures
RETRY_BACKOFF_MINUTES = [15, 30, 60]  # Exponential backoff intervals in minutes
MAX_CONSECUTIVE_FAILURES = 3  # Mark unavailable after this many failures

# Entity naming patterns for consistent entity IDs
ENTITY_ID_FORMAT_VENUE = "villages_events_{venue_slug}_{period}"
ENTITY_ID_FAVORITE_TODAY = "villages_events_favorite_today"
ENTITY_ID_FAVORITE_TOMORROW = "villages_events_favorite_tomorrow"

# Time period identifiers
PERIOD_TODAY = "today"
PERIOD_TOMORROW = "tomorrow"

# Attribute keys for entity state attributes
ATTR_VENUE = "venue"  # Venue name
ATTR_PERIOD = "period"  # Time period (today/tomorrow)
ATTR_EVENTS = "events"  # List of events
ATTR_LAST_UPDATED = "last_updated"  # Timestamp of last update
ATTR_PERFORMER = "performer"  # Performer name
ATTR_START_TIME = "start_time"  # Event start time
ATTR_END_TIME = "end_time"  # Event end time
ATTR_EVENT_TYPE = "event_type"  # Type of event (e.g., "Live Music")
ATTR_FAVORITE_PERFORMERS = "favorite_performers"  # List of configured favorites
ATTR_MATCHING_EVENTS = "matching_events"  # Events matching favorite performers
ATTR_COUNT = "count"  # Count of matching events

# Units of measurement
UNIT_EVENTS = "events"  # Unit for event count sensors
