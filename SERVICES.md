# Services Reference

The Villages Events integration provides services that can be called from automations, scripts, or the Developer Tools.

## Available Services

### `villages_events.refresh`

Manually refresh event data from The Villages calendar.

**Description:**
This service triggers an immediate data refresh, bypassing the normal update interval. All coordinators will fetch the latest event data, update all sensors, and fire any relevant events.

**Parameters:**
None

**Returns:**
None (service completes when refresh is done)

**Example Usage:**

#### In Automations

```yaml
automation:
  - alias: "Refresh Events Every Morning"
    description: "Get fresh event data at 8 AM daily"
    trigger:
      - platform: time
        at: "08:00:00"
    action:
      - service: villages_events.refresh
```

#### In Scripts

```yaml
script:
  refresh_and_notify:
    alias: "Refresh Events and Notify"
    sequence:
      - service: villages_events.refresh
      - delay:
          seconds: 3
      - service: notify.mobile_app
        data:
          title: "Events Updated"
          message: "Latest event data has been fetched"
```

#### From Developer Tools

1. Go to **Developer Tools** → **Services**
2. Search for "Villages Events: Refresh Events"
3. Click **Call Service**

#### With Home Assistant REST API

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_LONG_LIVED_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  http://homeassistant.local:8123/api/services/villages_events/refresh
```

## Use Cases

### 1. Scheduled Refresh

Refresh data at specific times when you know the schedule might change:

```yaml
automation:
  - alias: "Refresh Events Multiple Times Daily"
    trigger:
      - platform: time
        at:
          - "08:00:00"  # Morning
          - "12:00:00"  # Noon
          - "17:00:00"  # Evening
    action:
      - service: villages_events.refresh
```

### 2. Refresh Before Checking Events

Ensure you have the latest data before making decisions:

```yaml
automation:
  - alias: "Check Events Before Going Out"
    trigger:
      - platform: state
        entity_id: person.john
        to: "home"
        for:
          minutes: 30
    action:
      # Refresh data first
      - service: villages_events.refresh
      # Wait for refresh
      - delay:
          seconds: 5
      # Check if there are events tonight
      - condition: template
        value_template: >
          {{ states('sensor.villages_events_spanish_springs_today') | int > 0 }}
      # Notify about events
      - service: notify.mobile_app
        data:
          title: "Events Tonight!"
          message: "There are events at Spanish Springs tonight"
```

### 3. Manual Refresh Button

Create a button in your dashboard to refresh on demand:

**Step 1:** Create an input button helper:
```yaml
input_button:
  refresh_villages_events:
    name: Refresh Villages Events
    icon: mdi:refresh
```

**Step 2:** Create automation:
```yaml
automation:
  - alias: "Manual Refresh Villages Events"
    trigger:
      - platform: state
        entity_id: input_button.refresh_villages_events
    action:
      - service: villages_events.refresh
      - service: notify.persistent_notification
        data:
          title: "Villages Events"
          message: "Event data refreshed at {{ now().strftime('%I:%M %p') }}"
```

**Step 3:** Add button to dashboard:
```yaml
type: button
entity: input_button.refresh_villages_events
name: Refresh Events
icon: mdi:calendar-refresh
tap_action:
  action: call-service
  service: villages_events.refresh
```

### 4. Refresh After System Restart

Ensure fresh data after Home Assistant restarts:

```yaml
automation:
  - alias: "Refresh Events After Restart"
    trigger:
      - platform: homeassistant
        event: start
    action:
      # Wait for system to stabilize
      - delay:
          seconds: 30
      # Refresh event data
      - service: villages_events.refresh
```

### 5. Conditional Refresh Based on Time

Only refresh during certain hours to avoid unnecessary API calls:

```yaml
automation:
  - alias: "Smart Event Refresh"
    trigger:
      - platform: time_pattern
        hours: "/2"  # Every 2 hours
    condition:
      - condition: time
        after: "08:00:00"
        before: "23:00:00"
    action:
      - service: villages_events.refresh
```

### 6. Refresh When Arriving Home

Get latest events when you arrive home:

```yaml
automation:
  - alias: "Refresh Events When Home"
    trigger:
      - platform: state
        entity_id: person.john
        to: "home"
    action:
      - service: villages_events.refresh
      - delay:
          seconds: 5
      - service: tts.google_say
        data:
          entity_id: media_player.living_room
          message: >
            Welcome home! There are 
            {{ states('sensor.villages_events_spanish_springs_today') | int }}
            events at Spanish Springs today.
```

### 7. Refresh and Create Notification

Combine refresh with immediate notification:

```yaml
automation:
  - alias: "Evening Event Check"
    trigger:
      - platform: time
        at: "17:00:00"
    action:
      - service: villages_events.refresh
      - delay:
          seconds: 5
      - choose:
          - conditions:
              - condition: template
                value_template: >
                  {{ state_attr('binary_sensor.villages_events_favorite_today', 'count') | int > 0 }}
            sequence:
              - service: notify.mobile_app
                data:
                  title: "🎵 Favorite Performer Tonight!"
                  message: >
                    {% for event in state_attr('binary_sensor.villages_events_favorite_today', 'matching_events') %}
                      {{ event.performer }} at {{ event.venue }}
                    {% endfor %}
        default:
          - service: notify.mobile_app
            data:
              title: "Tonight's Events"
              message: >
                {{ states('sensor.villages_events_spanish_springs_today') | int }}
                events at Spanish Springs tonight
```

## Best Practices

### 1. Add Delays After Refresh

When you need to use the refreshed data immediately, add a small delay:

```yaml
- service: villages_events.refresh
- delay:
    seconds: 3
- service: notify.mobile_app
  data:
    message: "{{ states('sensor.villages_events_spanish_springs_today') }}"
```

### 2. Don't Over-Refresh

The integration already updates automatically based on your configured interval. Only use manual refresh when:
- You need immediate updates for a specific automation
- You want to refresh at specific times (morning, evening)
- User manually requests a refresh

### 3. Combine with Conditions

Check if a refresh is actually needed:

```yaml
automation:
  - alias: "Smart Refresh"
    trigger:
      - platform: time
        at: "18:00:00"
    condition:
      # Only refresh if data is older than 2 hours
      - condition: template
        value_template: >
          {{ (now() - states.sensor.villages_events_spanish_springs_today.last_updated).total_seconds() > 7200 }}
    action:
      - service: villages_events.refresh
```

### 4. Error Handling

The service will log errors if the refresh fails, but your automation will continue. Check logs if refreshes aren't working:

```yaml
logger:
  logs:
    custom_components.villages_events: debug
```

## Troubleshooting

### Service Not Found

**Problem:** Service `villages_events.refresh` doesn't appear in Developer Tools

**Solutions:**
- Restart Home Assistant completely
- Check that the integration is loaded: **Settings** → **Devices & Services**
- Check logs for integration errors

### Refresh Doesn't Update Sensors

**Problem:** Calling the service doesn't update sensor values

**Solutions:**
- Add a delay after calling the service before checking sensor values
- Check logs for errors during refresh
- Verify the integration is using real data (not mock data)
- Check that the update actually fetched new data (compare timestamps)

### Too Many Refreshes

**Problem:** Concerned about calling the API too frequently

**Solutions:**
- The integration respects the configured update interval
- Manual refreshes are additional to automatic updates
- Consider increasing the update interval and using manual refreshes strategically
- Add conditions to prevent unnecessary refreshes

## Related Documentation

- [Automation Examples](README.md#automation-examples)
- [Events Reference](EVENTS.md)
- [Developer Documentation](DEVELOPER.md)
