# The Villages Events - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

A Home Assistant custom integration that brings entertainment event information from The Villages, Florida directly to your dashboard. Track live performances at all venues, get notified when your favorite performers are scheduled, and plan your entertainment with ease.

## Features

- **Per-Venue Event Sensors**: Separate sensors for each venue showing today's and tomorrow's events
- **Favorite Performer Tracking**: Binary sensors that alert you when your favorite artists are scheduled
- **Automatic Updates**: Configurable update intervals to keep event information current
- **Rich Event Details**: View performer names, event times, and venue information
- **HACS Compatible**: Easy installation and automatic updates through HACS
- **UI Configuration**: No YAML editing required - configure everything through the UI

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
- `last_updated`: Timestamp of last data update

### Binary Sensor Entities

If you configure favorite performers, the integration creates:

- `binary_sensor.villages_events_favorite_today` - ON when a favorite performer plays today
- `binary_sensor.villages_events_favorite_tomorrow` - ON when a favorite performer plays tomorrow

**State**: ON (favorite performing) or OFF (no favorites scheduled)
**Attributes**:
- `favorite_performers`: Your configured list of favorites
- `matching_events`: Details of events featuring your favorites
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

### Notify When Favorite Performer Is Scheduled

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

### Daily Event Summary

```yaml
automation:
  - alias: "Daily Villages Events Summary"
    trigger:
      - platform: time
        at: "09:00:00"
    action:
      - service: notify.mobile_app
        data:
          title: "Today's Entertainment"
          message: >
            {% set total = states('sensor.villages_events_spanish_springs_today') | int + 
                          states('sensor.villages_events_brownwood_today') | int + 
                          states('sensor.villages_events_lake_sumter_today') | int %}
            {{ total }} events scheduled today at The Villages!
```

## Troubleshooting

### Integration Not Showing Events

**Problem**: Sensors show "0" or "unavailable"

**Solutions**:
- Check your internet connection
- Verify The Villages calendar website is accessible
- Check Home Assistant logs for error messages: **Settings** → **System** → **Logs**
- Try reloading the integration: **Settings** → **Devices & Services** → **The Villages Events** → **⋮** → **Reload**

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

## Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Check existing issues for similar problems
- Include Home Assistant version and integration version in bug reports
- Attach relevant log entries when reporting errors

## Credits

This integration uses the [python-villages-events](https://github.com/yourusername/python-villages-events) library to fetch event data from The Villages calendar.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
