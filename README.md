# The Villages Events - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/yourusername/villages-events-integration/releases)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A Home Assistant custom integration that brings entertainment event information from The Villages, Florida directly to your dashboard. Track live performances at all venues, get notified when your favorite performers are scheduled, and plan your entertainment with ease.

## Features

- **Per-Venue Event Sensors**: Separate sensors for each venue showing today's and tomorrow's events
- **Favorite Performer Tracking**: Binary sensors that alert you when your favorite artists are scheduled
- **Automatic Updates**: Configurable update intervals to keep event information current
- **Rich Event Details**: View performer names, event times, and venue information
- **HACS Compatible**: Easy installation and automatic updates through HACS
- **UI Configuration**: No YAML editing required - configure everything through the UI

## 📚 Documentation

- **[Complete Documentation](docs/README.md)** - Full documentation index
- [Installation & Configuration](#installation) - Get started
- [Entities & Attributes](#entities) - Available sensors and data
- [Dashboard Examples](#dashboard-examples) - UI card examples
- [Automation Examples](#automation-examples) - Automation ideas

### Quick Links
- [Services](docs/SERVICES.md) - Manual refresh service
- [Events](docs/EVENTS.md) - Home Assistant events for automations
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions
- [Developer Guide](docs/DEVELOPER.md) - For developers
- [Changelog](docs/CHANGELOG.md) - Version history

## Installation

### HACS Installation (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL and select "Integration" as the category
6. Click "Install"
7. Restart Home Assistant

### Manual Installation

1. Download the latest release from the releases page
2. Extract the `villages_events` folder from the zip file
3. Copy the folder to your `custom_components` directory
4. Restart Home Assistant

## Configuration

### Initial Setup

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "The Villages Events"
4. Configure the integration:
   - **Update Interval**: How often to fetch new event data (15-1440 minutes, default: 60)
   - **Favorite Performers**: Comma-separated list of performer names to track (optional)

### Example Configuration

```
Update Interval: 60 minutes
Favorite Performers: The Fabulous Fleetwoods, Retro Express, The British Invasion
```

### Reconfiguration

To change settings after initial setup:

1. Go to **Settings** → **Devices & Services**
2. Find "The Villages Events" integration
3. Click **Configure**
4. Update your settings
5. Click **Submit**

## Services

### `villages_events.refresh`

Manually refresh event data from The Villages calendar. This bypasses the normal update interval and fetches the latest events immediately.

**Usage in Automations:**

```yaml
automation:
  - alias: "Refresh Events Every Morning"
    trigger:
      - platform: time
        at: "08:00:00"
    action:
      - service: villages_events.refresh
```

**Usage in Scripts:**

```yaml
script:
  refresh_villages_events:
    alias: "Refresh Villages Events"
    sequence:
      - service: villages_events.refresh
```

**Call from Developer Tools:**

Go to **Developer Tools** → **Services**, search for "Villages Events: Refresh Events", and click "Call Service".

## Entities Created

### Sensor Entities

The integration creates sensor entities for each venue with today's and tomorrow's events:

- `sensor.villages_events_{venue}_today` - Events scheduled today at the venue
- `sensor.villages_events_{venue}_tomorrow` - Events scheduled tomorrow at the venue

**State**: Number of events scheduled
**Attributes**:
- `venue`: Venue name
- `period`: "today" or "tomorrow"
- `events`: List of event details (performer, start_time, end_time, event_type)
- `performers`: List of performer names (easy access)
- `event_count`: Number of events
- `last_updated`: Timestamp of last data update

### Binary Sensor Entities

If you configure favorite performers, the integration creates:

- `binary_sensor.villages_events_favorite_today` - ON when a favorite performer plays today
- `binary_sensor.villages_events_favorite_tomorrow` - ON when a favorite performer plays tomorrow

**State**: ON (favorite performing) or OFF (no favorites scheduled)
**Attributes**:
- `favorite_performers`: Your configured list of favorites
- `matching_events`: Details of events featuring your favorites
- `performers`: List of matching performer names (easy access)
- `venues`: List of venues where favorites are playing (easy access)
- `count`: Number of matching events

## Dashboard Examples

### Simple Event Card

```yaml
type: entities
title: Spanish Springs Tonight
entities:
  - entity: sensor.villages_events_spanish_springs_today
    secondary_info: last-updated
```

### Simple Performer List

```yaml
type: markdown
content: >
  ## Spanish Springs Tonight
  
  {% if states('sensor.villages_events_spanish_springs_today') | int > 0 %}
    **Performers:**
    {% for performer in state_attr('sensor.villages_events_spanish_springs_today', 'performers') %}
      - {{ performer }}
    {% endfor %}
  {% else %}
    No events scheduled today
  {% endif %}
```

### Detailed Event Card with Attributes

```yaml
type: markdown
content: >
  ## {{ state_attr('sensor.villages_events_spanish_springs_today', 'venue') }}
  
  {% if states('sensor.villages_events_spanish_springs_today') | int > 0 %}
    {% for event in state_attr('sensor.villages_events_spanish_springs_today', 'events') %}
      **{{ event.performer }}**  
      {{ event.start_time | as_timestamp | timestamp_custom('%I:%M %p') }} - 
      {{ event.end_time | as_timestamp | timestamp_custom('%I:%M %p') }}  
      {{ event.event_type }}
      
      ---
    {% endfor %}
  {% else %}
    No events scheduled today
  {% endif %}
```

### Favorite Performer Alert Card

```yaml
type: conditional
conditions:
  - entity: binary_sensor.villages_events_favorite_today
    state: 'on'
card:
  type: markdown
  content: >
    ## 🎵 Your Favorites Are Playing Today!
    
    {% for event in state_attr('binary_sensor.villages_events_favorite_today', 'matching_events') %}
      **{{ event.performer }}** at {{ event.venue }}  
      {{ event.start_time | as_timestamp | timestamp_custom('%I:%M %p') }}
      
    {% endfor %}
```

### Multi-Venue Overview

```yaml
type: vertical-stack
cards:
  - type: entities
    title: Today's Events
    entities:
      - sensor.villages_events_spanish_springs_today
      - sensor.villages_events_brownwood_today
      - sensor.villages_events_lake_sumter_today
  - type: entities
    title: Tomorrow's Events
    entities:
      - sensor.villages_events_spanish_springs_tomorrow
      - sensor.villages_events_brownwood_tomorrow
      - sensor.villages_events_lake_sumter_tomorrow
```

## Automation Examples

### Using Events (Recommended)

The integration fires Home Assistant events that you can use in automations:

#### Event: `villages_events_favorite_performer`

Fired when a favorite performer is newly detected.

**Event Data:**
- `period`: "today" or "tomorrow"
- `event_count`: Number of matching events
- `events`: List of event details
- `favorite_performers`: Your configured favorites

```yaml
automation:
  - alias: "Notify Favorite Performer Detected"
    trigger:
      - platform: event
        event_type: villages_events_favorite_performer
    action:
      - service: notify.mobile_app
        data:
          title: "🎵 Favorite Performer Alert!"
          message: >
            {% for event in trigger.event.data.events %}
              {{ event.performer }} at {{ event.venue }} {{ trigger.event.data.period }}
              at {{ event.start_time | as_timestamp | timestamp_custom('%I:%M %p') }}
            {% endfor %}
```

#### Event: `villages_events_new_events`

Fired when new events are detected at any venue.

**Event Data:**
- `venue`: Venue name
- `period`: "today" or "tomorrow"
- `event_count`: Total number of events
- `new_count`: Number of new events
- `events`: List of all events

```yaml
automation:
  - alias: "Notify New Events at Spanish Springs"
    trigger:
      - platform: event
        event_type: villages_events_new_events
        event_data:
          venue: "Spanish Springs Town Square"
    action:
      - service: notify.mobile_app
        data:
          title: "New Events at {{ trigger.event.data.venue }}"
          message: >
            {{ trigger.event.data.new_count }} new event(s) added for {{ trigger.event.data.period }}!
            Total: {{ trigger.event.data.event_count }} events
```

### Using Performer Names in Automations

Send a notification with just the performer names:

```yaml
automation:
  - alias: "Daily Event Summary"
    trigger:
      - platform: time
        at: "08:00:00"
    condition:
      - condition: numeric_state
        entity_id: sensor.villages_events_spanish_springs_today
        above: 0
    action:
      - service: notify.mobile_app
        data:
          title: "Tonight at Spanish Springs"
          message: >
            Performers: {{ state_attr('sensor.villages_events_spanish_springs_today', 'performers') | join(', ') }}
```

Check if a specific performer is playing:

```yaml
automation:
  - alias: "Check for Specific Performer"
    trigger:
      - platform: state
        entity_id: sensor.villages_events_spanish_springs_today
    condition:
      - condition: template
        value_template: >
          {{ 'The Beatles' in state_attr('sensor.villages_events_spanish_springs_today', 'performers') }}
    action:
      - service: notify.mobile_app
        data:
          title: "The Beatles are playing!"
          message: "Don't miss them at Spanish Springs tonight!"
```

### Using State Changes

You can also trigger automations based on entity state changes:

#### Notify When Favorite Performer Is Scheduled

```yaml
automation:
  - alias: "Notify Favorite Performer Today"
    trigger:
      - platform: state
        entity_id: binary_sensor.villages_events_favorite_today
        to: 'on'
    action:
      - service: notify.mobile_app
        data:
          title: "Your Favorite Performer is Playing!"
          message: >
            {% for event in state_attr('binary_sensor.villages_events_favorite_today', 'matching_events') %}
              {{ event.performer }} at {{ event.venue }} - {{ event.start_time | as_timestamp | timestamp_custom('%I:%M %p') }}
            {% endfor %}
```

### Daily Event Summary with Refresh

```yaml
automation:
  - alias: "Daily Villages Events Summary"
    trigger:
      - platform: time
        at: "09:00:00"
    action:
      # First refresh the data
      - service: villages_events.refresh
      # Wait for refresh to complete
      - delay:
          seconds: 5
      # Then send notification with latest data
      - service: notify.mobile_app
        data:
          title: "Today's Entertainment"
          message: >
            {% set total = states('sensor.villages_events_spanish_springs_today') | int + 
                          states('sensor.villages_events_brownwood_today') | int + 
                          states('sensor.villages_events_lake_sumter_today') | int %}
            {{ total }} events scheduled today at The Villages!
```

### Refresh on Demand with Button

```yaml
automation:
  - alias: "Refresh Events Button"
    trigger:
      - platform: state
        entity_id: input_button.refresh_villages_events
    action:
      - service: villages_events.refresh
      - service: notify.persistent_notification
        data:
          title: "Villages Events"
          message: "Event data refreshed successfully!"
```

### Advanced Event-Based Automations

#### Create Calendar Entries for Favorite Performers

```yaml
automation:
  - alias: "Add Favorite Performer to Calendar"
    trigger:
      - platform: event
        event_type: villages_events_favorite_performer
    action:
      - repeat:
          for_each: "{{ trigger.event.data.events }}"
          sequence:
            - service: calendar.create_event
              target:
                entity_id: calendar.personal
              data:
                summary: "{{ repeat.item.performer }} at The Villages"
                description: "{{ repeat.item.event_type }} at {{ repeat.item.venue }}"
                start_date_time: "{{ repeat.item.start_time }}"
                end_date_time: "{{ repeat.item.end_time }}"
```

#### Send Rich Notification with Action Buttons

```yaml
automation:
  - alias: "Favorite Performer with Actions"
    trigger:
      - platform: event
        event_type: villages_events_favorite_performer
    action:
      - service: notify.mobile_app
        data:
          title: "🎵 {{ trigger.event.data.events[0].performer }}"
          message: >
            Playing {{ trigger.event.data.period }} at {{ trigger.event.data.events[0].venue }}
            {{ trigger.event.data.events[0].start_time | as_timestamp | timestamp_custom('%I:%M %p') }}
          data:
            actions:
              - action: "ADD_TO_CALENDAR"
                title: "Add to Calendar"
              - action: "VIEW_VENUE"
                title: "View Venue Info"
```

#### Log All New Events to Logbook

```yaml
automation:
  - alias: "Log New Events"
    trigger:
      - platform: event
        event_type: villages_events_new_events
    action:
      - service: logbook.log
        data:
          name: "Villages Events"
          message: >
            {{ trigger.event.data.new_count }} new event(s) at {{ trigger.event.data.venue }} 
            for {{ trigger.event.data.period }}
          entity_id: sensor.villages_events_{{ trigger.event.data.venue | lower | replace(' ', '_') }}_{{ trigger.event.data.period }}
```

## Data Source

This integration includes built-in code to fetch real event data from The Villages entertainment calendar API. No external libraries are required!

### Live Data

The integration automatically fetches live event data from The Villages calendar. Simply install the integration and it will start pulling real events.

**What you'll see in the logs:**
```
Successfully fetched events for X venues
```

### Development Mode (Fallback)

If there are any issues connecting to The Villages API, the integration will automatically fall back to mock data for testing. You'll see a warning:

```
Villages events library import failed. Using mock data for development/testing.
```

This ensures the integration continues to work even if The Villages website is temporarily unavailable.

## Troubleshooting

### Integration Not Showing Events

**Problem**: Sensors show "0" or "unavailable"

**Solutions**:
- Check your internet connection
- Verify The Villages calendar website is accessible
- Check Home Assistant logs for error messages: **Settings** → **System** → **Logs**
- Try reloading the integration: **Settings** → **Devices & Services** → **The Villages Events** → **⋮** → **Reload**
- If using development mode, check that mock data is being loaded (look for "Using mock data" in logs)

### Favorite Performers Not Detected

**Problem**: Binary sensor stays OFF even though your favorite is scheduled

**Solutions**:
- Verify the performer name matches exactly as it appears on The Villages calendar
- Check for extra spaces or punctuation in your configuration
- Performer names are case-insensitive but must match otherwise
- Reconfigure the integration and update your favorite performers list

### Update Interval Too Frequent

**Problem**: Integration updates too often or not often enough

**Solutions**:
- Reconfigure the integration and adjust the update interval
- Minimum: 15 minutes (to avoid excessive API calls)
- Maximum: 1440 minutes (24 hours)
- Recommended: 60 minutes for good balance

### Entities Not Created

**Problem**: Expected sensor entities are missing

**Solutions**:
- Restart Home Assistant after installation
- Check that the integration loaded successfully in logs
- Verify the integration appears in **Settings** → **Devices & Services**
- Try removing and re-adding the integration

### Error: "Update Failed"

**Problem**: Logs show repeated update failures

**Solutions**:
- The integration will retry automatically with exponential backoff
- After 3 consecutive failures, entities will be marked unavailable
- Check if The Villages website is accessible from your network
- Verify the `python-villages-events` library is installed correctly
- Wait for automatic recovery when connectivity is restored

## Documentation

- **[Services Reference](SERVICES.md)** - Detailed guide for the `villages_events.refresh` service
- **[Events Reference](EVENTS.md)** - Complete guide for event-based automations
- **[Developer Documentation](DEVELOPER.md)** - Architecture and development guide
- **[Debugging Guide](DEBUG.md)** - Troubleshooting and debugging steps

## Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Check existing issues for similar problems
- Include Home Assistant version and integration version in bug reports
- Attach relevant log entries when reporting errors

## Credits

This integration uses the [python-villages-events](https://github.com/netnutmike/python-villages-events) library to fetch event data from The Villages calendar.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
