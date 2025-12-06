# Troubleshooting Guide

## Config Flow Error: "500 Internal Server Error"

If you get a "Config flow could not be loaded: 500 Internal Server Error" when trying to edit integration options:

### Solution 1: Clear Python Cache

Home Assistant may be using cached bytecode. See [CLEAR_CACHE.md](CLEAR_CACHE.md) for detailed instructions.

Quick fix:
```bash
cd /config/custom_components/villages_events
find . -type d -name __pycache__ -exec rm -rf {} +
find . -name "*.pyc" -delete
```

Then restart Home Assistant.

### Solution 2: Restart Home Assistant

Config flow changes require a **full restart** of Home Assistant, not just a reload:

1. Go to **Settings** → **System** → **Restart**
2. Click **Restart Home Assistant**
3. Wait for Home Assistant to fully restart
4. Try opening the integration options again

### Solution 2: Check Home Assistant Logs

View the logs to see the actual error:

1. Go to **Settings** → **System** → **Logs**
2. Look for errors related to `villages_events` or `config_flow`
3. The error message will show what's actually failing

### Solution 3: Check Config Entry Data

The error might be caused by corrupted config entry data. To check:

1. Go to **Developer Tools** → **States**
2. Look for entities starting with `sensor.villages_events_`
3. Check if they have valid data

### Solution 4: Remove and Re-add Integration

If the above doesn't work, you may need to remove and re-add the integration:

1. Go to **Settings** → **Devices & Services**
2. Find "The Villages Events"
3. Click the three dots → **Delete**
4. Click **Add Integration**
5. Search for "The Villages Events"
6. Configure with your settings

**Note**: This will remove all entities and you'll need to update any automations/dashboards that reference them.

## Common Issues

### No Events Showing

**Problem**: Sensors show 0 events or "Unknown"

**Solutions**:
1. Check if there are actually events scheduled today/tomorrow
2. Verify internet connection
3. Check Home Assistant logs for API errors
4. Reload the integration: **Settings** → **Devices & Services** → **Villages Events** → **Reload**

### Favorite Performers Not Working

**Problem**: Binary sensors don't detect favorite performers

**Solutions**:
1. Check spelling of performer names (case-insensitive matching)
2. Use partial names (e.g., "Beatles" will match "The Beatles")
3. Check the sensor attributes to see what performers are scheduled
4. Edit integration options to update favorite performers list

### Entities Unavailable

**Problem**: All entities show as "Unavailable"

**Solutions**:
1. Check Home Assistant logs for errors
2. Verify The Villages API is accessible
3. Wait for next update cycle (default: 60 minutes)
4. Manually refresh: Call service `villages_events.refresh`

### Update Interval Not Working

**Problem**: Data doesn't update at configured interval

**Solutions**:
1. Check that update interval is between 15-1440 minutes
2. Restart Home Assistant after changing interval
3. Check logs for update errors
4. Manually trigger update with `villages_events.refresh` service

## Getting Help

If you're still having issues:

1. **Check Logs**: Always check Home Assistant logs first
2. **Provide Details**: Include:
   - Home Assistant version
   - Integration version
   - Error messages from logs
   - Steps to reproduce the issue
3. **GitHub Issues**: Report bugs at the integration's GitHub repository

## Debug Mode

To enable debug logging for this integration:

1. Edit `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.villages_events: debug
```

2. Restart Home Assistant
3. Check logs for detailed debug information
4. Remember to remove debug logging when done (it can be verbose)
