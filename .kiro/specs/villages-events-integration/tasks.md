# Implementation Plan

- [x] 1. Set up repository structure and HACS configuration
  - Create directory structure for custom_components/villages_events/
  - Create hacs.json with integration metadata
  - Create info.md for HACS store display
  - Create renovate.json for dependency management
  - _Requirements: 1.1, 1.3, 1.4, 1.5, 7.1, 7.2, 7.3_

- [x] 2. Create integration manifest and constants
  - Write manifest.json with integration metadata, dependencies, and version
  - Create const.py with domain, configuration keys, and default values
  - Define platform constants (SENSOR, BINARY_SENSOR)
  - _Requirements: 1.4, 7.3_

- [x] 3. Implement configuration flow
  - [x] 3.1 Create config_flow.py with ConfigFlow class
    - Implement async_step_user for initial configuration
    - Add input validation for update interval (15-1440 minutes)
    - Add input validation for favorite performers list
    - Create config entry on successful validation
    - _Requirements: 2.1, 2.2, 2.4_
  
  - [x] 3.2 Implement options flow for reconfiguration
    - Add async_step_init for options flow
    - Allow users to update interval and favorite performers
    - Trigger coordinator reload on options change
    - _Requirements: 2.1, 2.4_
  
  - [x] 3.3 Create strings.json and translations
    - Define UI strings for configuration flow
    - Create translations/en.json with English translations
    - Add error message strings for validation failures
    - _Requirements: 2.2_

- [x] 4. Implement data update coordinator
  - [x] 4.1 Create coordinator.py with VillagesEventsCoordinator class
    - Extend DataUpdateCoordinator from Home Assistant
    - Initialize with hass, config entry, and update interval
    - Store favorite performers list from configuration
    - _Requirements: 3.1, 3.3_
  
  - [x] 4.2 Implement _async_update_data method
    - Fetch events from python-villages-events library using executor
    - Calculate today and tomorrow dates based on HA timezone
    - Parse and structure event data by venue
    - Group events into today and tomorrow categories per venue
    - _Requirements: 3.1, 3.3, 4.2_
  
  - [x] 4.3 Implement favorite performer matching logic
    - Compare event performers against favorite performers list
    - Create favorite_today and favorite_tomorrow boolean flags
    - Build favorite_events dictionary with matching events
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_
  
  - [x] 4.4 Add error handling and retry logic
    - Catch network errors and maintain last known state
    - Implement exponential backoff for retries (15, 30, 60 minutes)
    - Track consecutive failures and mark unavailable after 3 failures
    - Log errors with appropriate severity levels
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 5. Implement sensor platform for venue events
  - [x] 5.1 Create sensor.py with async_setup_entry function
    - Retrieve coordinator from hass.data
    - Create VillagesEventSensor entities for each venue and period
    - Add entities to Home Assistant
    - _Requirements: 2.3, 3.2_
  
  - [x] 5.2 Implement VillagesEventSensor class
    - Extend CoordinatorEntity and SensorEntity
    - Set entity naming format: villages_events_{venue_slug}_{period}
    - Implement state property returning event count
    - Set unit_of_measurement to "events"
    - _Requirements: 3.2, 3.4, 3.5_
  
  - [x] 5.3 Implement sensor attributes
    - Add venue name, period (today/tomorrow), and events list
    - Include performer, start_time, end_time, event_type for each event
    - Add last_updated timestamp
    - Handle unavailable state when coordinator fails
    - _Requirements: 3.5, 4.3, 5.4_

- [x] 6. Implement binary sensor platform for favorite performers
  - [x] 6.1 Create binary_sensor.py with async_setup_entry function
    - Retrieve coordinator from hass.data
    - Create VillagesFavoritePerformerSensor for today and tomorrow
    - Add entities to Home Assistant
    - _Requirements: 2.3, 6.2, 6.3_
  
  - [x] 6.2 Implement VillagesFavoritePerformerSensor class
    - Extend CoordinatorEntity and BinarySensorEntity
    - Set device_class to "presence"
    - Implement is_on property based on favorite performer matches
    - Create entities: villages_events_favorite_today and villages_events_favorite_tomorrow
    - _Requirements: 6.2, 6.3, 6.6_
  
  - [x] 6.3 Implement binary sensor attributes
    - Add favorite_performers list from configuration
    - Include matching_events with performer, venue, and time details
    - Add count of matching events
    - Handle unavailable state when coordinator fails
    - _Requirements: 6.4, 6.5_

- [x] 7. Implement integration entry point
  - [x] 7.1 Create __init__.py with async_setup_entry function
    - Extract configuration from config entry
    - Create VillagesEventsCoordinator instance
    - Perform initial data fetch
    - Store coordinator in hass.data
    - Forward setup to sensor and binary_sensor platforms
    - _Requirements: 2.3, 3.1, 3.3_
  
  - [x] 7.2 Implement async_unload_entry function
    - Unload sensor and binary_sensor platforms
    - Clean up coordinator resources
    - Remove data from hass.data
    - _Requirements: 2.3_
  
  - [x] 7.3 Implement async_reload_entry function
    - Call async_unload_entry
    - Call async_setup_entry with updated configuration
    - _Requirements: 2.3_

- [x] 8. Create user documentation
  - [x] 8.1 Write README.md
    - Add overview of integration features
    - Include HACS installation instructions
    - Document configuration options with examples
    - Provide dashboard card examples
    - Add troubleshooting section
    - _Requirements: 7.4_
  
  - [x] 8.2 Write LICENSE file
    - Add appropriate open source license (MIT recommended)
    - _Requirements: 7.5_

- [x] 9. Create developer documentation
  - [x] 9.1 Write DEVELOPER.md
    - Document architecture with component interaction diagram
    - Explain data flow from python-villages-events to entities
    - Describe development setup and testing procedures
    - Provide examples for adding new sensor types
    - Include examples for extending configuration options
    - Document code style standards and requirements
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_
  
  - [x] 9.2 Add inline code documentation
    - Write docstrings for all classes following Google style
    - Document all public methods with parameters and return types
    - Add type hints throughout the codebase
    - Include usage examples in docstrings where appropriate
    - _Requirements: 8.1_
