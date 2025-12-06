# Home Assistant Events Reference

The Villages Events integration fires Home Assistant events that can be used in automations to react to new events and favorite performer detections.

## Event Types

### `villages_events_favorite_performer`

Fired when a favorite performer is newly detected in the schedule.

**When it fires:**
- On first data fetch if favorites are present
- When a favorite performer is newly added to the schedule
- Separate events for "today" and "tomorrow"

**Event Data:**

| Field | Type | Description |
|-------|------|-------------|
| `period` | string | "today" or "tomorrow" |
| `event_count` | integer | Number of matching events |
| `events` | list | List of event dictionaries |
| `favorite_performers` | list | Your configured favorite performers |

**Event Dictionary Structure:**
```python
{
    "performer": "Artist Name",
    "venue": "Venue Name",
    "start_time": "2025-01-15T19:00:00",
    "end_time": "2025-01-15T21:00:00",
    "event_type": "Live Music"
}
```

**Example Automation:**
```yaml
automation:
  - alias: "Favorite Performer Alert"
    trigger:
      - platform: event
        event_type: villages_events_favorite_performer
    condition:
      - condition: template
        value_template: "{{ trigger.event.data.period == 'today' }}"
    action:
      - service: notify.mobile_app
        data:
          title: "Favorite Performer Tonight!"
          message: >
            {{ trigger.event.data.events[0].performer }} 
            at {{ trigger.event.data.events[0].venue }}
```

### `villages_events_new_events`

Fired when new events are detected at any venue.

**When it fires:**
- When the event count at a venue increases
- Separate events for each venue and period combination

**Event Data:**

| Field | Type | Description |
|-------|------|-------------|
| `venue` | string | Venue name |
| `period` | string | "today" or "tomorrow" |
| `event_count` | integer | Total number of events |
| `new_count` | integer | Number of new events detected |
| `events` | list | List of all event dictionaries |

**Event Dictionary Structure:**
```python
{
    "performer": "Artist Name",
    "start_time": "2025-01-15T19:00:00",
    "end_time": "2025-01-15T21:00:00",
    "event_type": "Live Music"
}
```

**Example Automation:**
```yaml
automation:
  - alias: "New Events at Any Venue"
    trigger:
      - platform: event
        event_type: villages_events_new_events
    action:
      - service: persistent_notification.create
        data:
          title: "New Events at {{ trigger.event.data.venue }}"
          message: >
            {{ trigger.event.data.new_count }} new event(s) for {{ trigger.event.data.period }}
```

## Filtering Events

### Filter by Venue

```yaml
automation:
  - alias: "Spanish Springs Only"
    trigger:
      - platform: event
        event_type: villages_events_new_events
        event_data:
          venue: "Spanish Springs Town Square"
    action:
      # Your actions here
```

### Filter by Period

```yaml
automation:
  - alias: "Today's Events Only"
    trigger:
      - platform: event
        event_type: villages_events_new_events
    condition:
      - condition: template
        value_template: "{{ trigger.event.data.period == 'today' }}"
    action:
      # Your actions here
```

### Filter by Event Count

```yaml
automation:
  - alias: "Multiple New Events"
    trigger:
      - platform: event
        event_type: villages_events_new_events
    condition:
      - condition: template
        value_template: "{{ trigger.event.data.new_count >= 3 }}"
    action:
      # Your actions here
```

## Advanced Use Cases

### Create Google Calendar Events

```yaml
automation:
  - alias: "Add Favorites to Google Calendar"
    trigger:
      - platform: event
        event_type: villages_events_favorite_performer
    action:
      - repeat:
          for_each: "{{ trigger.event.data.events }}"
          sequence:
            - service: google.add_event
              data:
                calendar_id: "your_calendar_id"
                summary: "{{ repeat.item.performer }}"
                description: "{{ repeat.item.event_type }} at {{ repeat.item.venue }}"
                start_date_time: "{{ repeat.item.start_time }}"
                end_date_time: "{{ repeat.item.end_time }}"
```

### Send to Multiple Notification Services

```yaml
automation:
  - alias: "Multi-Channel Favorite Alert"
    trigger:
      - platform: event
        event_type: villages_events_favorite_performer
    action:
      - parallel:
          - service: notify.mobile_app
            data:
              title: "Favorite Performer!"
              message: "{{ trigger.event.data.events[0].performer }}"
          - service: notify.alexa_media
            data:
              target: media_player.echo_dot
              message: "Your favorite performer {{ trigger.event.data.events[0].performer }} is playing {{ trigger.event.data.period }}"
          - service: telegram_bot.send_message
            data:
              message: "🎵 {{ trigger.event.data.events[0].performer }} at {{ trigger.event.data.events[0].venue }}"
```

### Update Input Select with Today's Performers

```yaml
automation:
  - alias: "Update Performer List"
    trigger:
      - platform: event
        event_type: villages_events_new_events
        event_data:
          period: "today"
    action:
      - service: input_select.set_options
        target:
          entity_id: input_select.todays_performers
        data:
          options: >
            {{ trigger.event.data.events | map(attribute='performer') | list }}
```

### Conditional Notifications Based on Time

```yaml
automation:
  - alias: "Favorite Performer - Time Aware"
    trigger:
      - platform: event
        event_type: villages_events_favorite_performer
    condition:
      - condition: time
        after: "08:00:00"
        before: "22:00:00"
    action:
      - service: notify.mobile_app
        data:
          title: "Favorite Performer Alert"
          message: "{{ trigger.event.data.events[0].performer }} is playing {{ trigger.event.data.period }}"
```

## Testing Events

To test event-based automations, you can manually fire events from Developer Tools → Events:

**Test Favorite Performer Event:**
```yaml
event_type: villages_events_favorite_performer
event_data:
  period: "today"
  event_count: 1
  events:
    - performer: "Test Artist"
      venue: "Spanish Springs Town Square"
      start_time: "2025-01-15T19:00:00"
      end_time: "2025-01-15T21:00:00"
      event_type: "Live Music"
  favorite_performers:
    - "test artist"
```

**Test New Events:**
```yaml
event_type: villages_events_new_events
event_data:
  venue: "Spanish Springs Town Square"
  period: "today"
  event_count: 3
  new_count: 1
  events:
    - performer: "Test Artist"
      start_time: "2025-01-15T19:00:00"
      end_time: "2025-01-15T21:00:00"
      event_type: "Live Music"
```

## Debugging

Enable debug logging to see when events are fired:

```yaml
logger:
  logs:
    custom_components.villages_events: debug
```

Look for log messages like:
- "Favorite performer(s) newly detected for today: X event(s)"
- "Detected X new event(s) at [venue] for [period]"
