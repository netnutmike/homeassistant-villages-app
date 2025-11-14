# The Villages Events Integration

Bring The Villages, Florida entertainment calendar to your Home Assistant dashboard!

## Features

- **Per-Venue Sensors**: Separate sensors for each entertainment venue showing today's and tomorrow's events
- **Favorite Performer Tracking**: Binary sensors that notify you when your favorite performers are scheduled
- **Automatic Updates**: Configurable update intervals to keep event information current
- **Rich Event Details**: View performer names, event times, and venue information
- **Easy Configuration**: Simple UI-based setup through Home Assistant's integration flow

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL and select "Integration" as the category
6. Click "Install"
7. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/villages_events` directory to your Home Assistant `custom_components` folder
2. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services
2. Click "+ Add Integration"
3. Search for "The Villages Events"
4. Configure your preferences:
   - **Update Interval**: How often to fetch new event data (15-1440 minutes, default: 60)
   - **Favorite Performers**: Comma-separated list of performer names to track (optional)

## Usage

After configuration, the integration creates:

### Venue Event Sensors
- `sensor.villages_events_{venue}_today` - Events scheduled today at each venue
- `sensor.villages_events_{venue}_tomorrow` - Events scheduled tomorrow at each venue

Each sensor shows the number of events and includes detailed attributes with performer information.

### Favorite Performer Sensors
- `binary_sensor.villages_events_favorite_today` - ON when a favorite performer plays today
- `binary_sensor.villages_events_favorite_tomorrow` - ON when a favorite performer plays tomorrow

### Dashboard Card Example

```yaml
type: entities
title: Today's Events
entities:
  - sensor.villages_events_spanish_springs_today
  - sensor.villages_events_lake_sumter_today
  - sensor.villages_events_brownwood_today
  - binary_sensor.villages_events_favorite_today
```

### Automation Example

```yaml
automation:
  - alias: "Notify when favorite performer is scheduled"
    trigger:
      - platform: state
        entity_id: binary_sensor.villages_events_favorite_tomorrow
        to: "on"
    action:
      - service: notify.mobile_app
        data:
          title: "Favorite Performer Alert"
          message: "{{ state_attr('binary_sensor.villages_events_favorite_tomorrow', 'matching_events')[0].performer }} is playing tomorrow!"
```

## Troubleshooting

**Integration not appearing**: Ensure you've restarted Home Assistant after installation.

**No data showing**: Check the Home Assistant logs for errors. The integration requires internet connectivity to fetch event data.

**Entities unavailable**: The integration marks entities unavailable after 3 consecutive fetch failures. Check your network connection and Home Assistant logs.

## Support

For issues, feature requests, or questions, please open an issue on GitHub.
