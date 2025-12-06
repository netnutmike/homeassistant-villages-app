# Debugging The Villages Events Integration

## Step 1: Enable Debug Logging

Add this to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.villages_events: debug
```

Then restart Home Assistant.

## Step 2: Check the Logs

Go to **Settings** → **System** → **Logs** or check the log file directly.

Look for messages containing `villages_events` to see:
- If the integration is loading
- If the coordinator is fetching data
- If entities are being created
- Any errors or warnings

## Step 3: Check Entity States

Go to **Developer Tools** → **States** and search for `villages_events` to see:
- Which entities were created
- Their current states
- Their attributes

## Step 4: Common Issues to Check

### Issue: No entities created
**Look for in logs:**
- "Set up X Villages Events sensor entities"
- "Set up X Villages Events binary sensor entities"

**If you see 0 entities:**
- Check that coordinator.data contains venues
- Check that the mock data is being returned

### Issue: Entities show "unavailable"
**Look for in logs:**
- "Maximum consecutive failures reached"
- Error messages in _async_update_data

**Check:**
- coordinator.is_unavailable property
- consecutive_failures counter

### Issue: Entities show "0" or empty
**Look for in logs:**
- "Successfully fetched events for X venues"
- "Using mock data with X venues"

**Check:**
- coordinator.data structure
- venues_data in coordinator

## Step 5: Manual Testing in Developer Tools

Go to **Developer Tools** → **Template** and test:

```jinja2
{# Check if integration is loaded #}
{{ integration_entities('villages_events') }}

{# Check a specific sensor #}
{{ states('sensor.villages_events_spanish_springs_today') }}
{{ state_attr('sensor.villages_events_spanish_springs_today', 'events') }}

{# Check binary sensor #}
{{ states('binary_sensor.villages_events_favorite_today') }}
{{ state_attr('binary_sensor.villages_events_favorite_today', 'matching_events') }}
```

## Step 6: Check Coordinator Data

Add temporary debug logging to see coordinator data. In `coordinator.py`, after the return statement in `_async_update_data`, the data should be logged.

## Expected Log Messages

When working correctly, you should see:

```
[custom_components.villages_events] Setting up The Villages Events integration
[custom_components.villages_events.coordinator] python-villages-events library not installed. Using mock data for development/testing.
[custom_components.villages_events.coordinator] Using mock data with 3 venues
[custom_components.villages_events] Successfully initialized The Villages Events coordinator with 3 venues
[custom_components.villages_events.sensor] Set up 6 Villages Events sensor entities
[custom_components.villages_events.binary_sensor] Set up 2 Villages Events binary sensor entities
```

## Quick Diagnostic Commands

If you have access to the Home Assistant CLI:

```bash
# Check if integration is loaded
ha core logs | grep villages_events

# Check entity registry
ha core entities | grep villages_events

# Restart integration
ha core restart
```
