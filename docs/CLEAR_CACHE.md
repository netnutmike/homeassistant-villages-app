# Clear Home Assistant Python Cache

If you're getting config flow errors with no logs, Home Assistant might be using cached Python bytecode. Here's how to clear it:

## Method 1: Delete __pycache__ Directories

1. Stop Home Assistant
2. Navigate to your custom_components directory:
   ```bash
   cd /config/custom_components/villages_events
   ```

3. Delete all __pycache__ directories:
   ```bash
   find . -type d -name __pycache__ -exec rm -rf {} +
   ```

4. Also delete any .pyc files:
   ```bash
   find . -name "*.pyc" -delete
   ```

5. Restart Home Assistant

## Method 2: Full Reinstall

1. Go to **Settings** → **Devices & Services**
2. Find "The Villages Events"
3. Click the three dots → **Delete**
4. Delete the integration folder:
   ```bash
   rm -rf /config/custom_components/villages_events
   ```
5. Reinstall the integration (via HACS or manually)
6. Restart Home Assistant
7. Add the integration again

## Method 3: Docker/Container Users

If running Home Assistant in Docker:

```bash
# Stop the container
docker stop homeassistant

# Remove Python cache
docker exec homeassistant find /config/custom_components/villages_events -type d -name __pycache__ -exec rm -rf {} +

# Restart the container
docker start homeassistant
```

## Method 4: Home Assistant OS

If using Home Assistant OS:

1. Install the **Terminal & SSH** add-on
2. Open the Terminal
3. Run:
   ```bash
   cd /config/custom_components/villages_events
   find . -type d -name __pycache__ -exec rm -rf {} +
   find . -name "*.pyc" -delete
   ```
4. Restart Home Assistant from the UI

## Verify the Fix

After clearing cache and restarting:

1. Go to **Settings** → **Devices & Services**
2. Find "The Villages Events"
3. Click the gear icon (Configure)
4. The options dialog should now open

## Still Not Working?

If you still get the error:

1. Enable debug logging in `configuration.yaml`:
   ```yaml
   logger:
     default: warning
     logs:
       custom_components.villages_events: debug
       homeassistant.config_entries: debug
   ```

2. Restart Home Assistant

3. Try opening the options again

4. Check **Settings** → **System** → **Logs** for detailed error messages

5. Share the error log for further assistance
