# How to View Home Assistant Logs Properly

The web interface log viewer is limited and filters many messages. Here are better ways to see ALL logs:

## Method 1: View Full Log File (Best for Debugging)

### Via SSH/Terminal:

```bash
# View the full log file
cat /config/home-assistant.log

# View last 100 lines
tail -100 /config/home-assistant.log

# Follow log in real-time (like tail -f)
tail -f /config/home-assistant.log

# Search for specific terms
grep -i "villages" /config/home-assistant.log
grep -i "config_flow" /config/home-assistant.log
grep -i "error" /config/home-assistant.log

# Search for villages events with context (5 lines before/after)
grep -i -A 5 -B 5 "villages" /config/home-assistant.log
```

### Via File Editor Add-on:

1. Install "File Editor" add-on if not installed
2. Navigate to `/config/home-assistant.log`
3. Open and search for "villages" or "config_flow"

## Method 2: Real-Time Log Monitoring

### Via Terminal & SSH Add-on:

```bash
# Watch logs in real-time
tail -f /config/home-assistant.log

# Filter for villages events only
tail -f /config/home-assistant.log | grep -i villages

# Filter for config flow errors
tail -f /config/home-assistant.log | grep -i "config_flow\|500\|error"
```

Then in another browser tab, try clicking the gear icon. You'll see the error appear in real-time!

## Method 3: Docker Logs (If Using Docker)

```bash
# View container logs
docker logs homeassistant

# Follow logs in real-time
docker logs -f homeassistant

# Last 100 lines
docker logs --tail 100 homeassistant

# Filter for villages
docker logs homeassistant 2>&1 | grep -i villages
```

## Method 4: System Journal (Home Assistant OS)

```bash
# View Home Assistant logs via journalctl
journalctl -u homeassistant -f

# Last 100 lines
journalctl -u homeassistant -n 100

# Filter for errors
journalctl -u homeassistant | grep -i error
```

## Method 5: Download Log File

### Via Web Interface:

1. Go to **Settings** → **System** → **Logs**
2. Click **Load Full Home Assistant Log** (top right)
3. Click **Download** button
4. Open the downloaded file in a text editor
5. Search for "villages" or "config_flow"

## What to Look For

When you click the gear icon and get the 500 error, look for:

### Python Errors:
```
Traceback (most recent call last):
  File "/config/custom_components/villages_events/config_flow.py"
  ...
```

### Import Errors:
```
Error loading custom_components.villages_events
ImportError: cannot import name 'something'
```

### Config Flow Errors:
```
Error setting up config flow for villages_events
```

### 500 Errors:
```
500 Internal Server Error
```

## Recommended Debugging Workflow

### Step 1: Start Log Monitoring

In SSH terminal:
```bash
tail -f /config/home-assistant.log | grep -i "villages\|config_flow\|500"
```

### Step 2: Trigger the Error

In your browser:
1. Go to Settings → Devices & Services
2. Find "The Villages Events"
3. Click the gear icon

### Step 3: Watch the Terminal

The error should appear immediately in the terminal showing the tail command.

### Step 4: Copy the Error

Copy the full error message including the traceback.

## Common Issues Why Logs Don't Show

### Issue 1: Log Level Too High

Your `configuration.yaml` should have:
```yaml
logger:
  default: info  # or debug
  logs:
    custom_components.villages_events: debug
    homeassistant.config_entries: debug
```

Not:
```yaml
logger:
  default: warning  # This filters out too much
```

### Issue 2: Logs Not Reloaded

After changing `configuration.yaml`:
1. **Restart Home Assistant** (full restart required)
2. Logs won't update until restart

### Issue 3: Wrong Log File

Make sure you're looking at:
- `/config/home-assistant.log` (current log)

Not:
- `/config/home-assistant.log.1` (old rotated log)

### Issue 4: Web Interface Filters

The web interface at Settings → System → Logs:
- Filters out many messages
- Only shows recent logs
- May not show all debug messages

**Solution:** Use `tail -f /config/home-assistant.log` instead

## Example: Finding Config Flow Error

```bash
# SSH into Home Assistant
ssh root@homeassistant.local

# Start monitoring logs
tail -f /config/home-assistant.log | grep -i "villages\|config_flow"

# In another window/tab, click the gear icon in HA

# You should see output like:
# 2024-12-06 18:30:15 ERROR (MainThread) [homeassistant.components.config] 
# Error handling request: 500 Internal Server Error
# 2024-12-06 18:30:15 ERROR (MainThread) [custom_components.villages_events.config_flow]
# Error in options flow: ...
```

## Quick Commands Reference

```bash
# View full log
cat /config/home-assistant.log

# Last 50 lines
tail -50 /config/home-assistant.log

# Follow in real-time
tail -f /config/home-assistant.log

# Search for villages
grep -i villages /config/home-assistant.log

# Search with context
grep -i -C 10 "config_flow" /config/home-assistant.log

# Count errors
grep -c ERROR /config/home-assistant.log

# Show only errors
grep ERROR /config/home-assistant.log

# Show errors and warnings
grep -E "ERROR|WARNING" /config/home-assistant.log
```

## After Finding the Error

Once you see the error in the logs:

1. **Copy the full traceback** (all lines starting with "Traceback")
2. **Note the error message** (last line of traceback)
3. **Check the file and line number** mentioned in the traceback
4. Share the error for help debugging

## Summary

**Best method for debugging:**
```bash
# In SSH terminal:
tail -f /config/home-assistant.log | grep -i villages

# Then click the gear icon in HA
# Error will appear immediately in terminal
```

This shows you the REAL error that the web interface hides!
