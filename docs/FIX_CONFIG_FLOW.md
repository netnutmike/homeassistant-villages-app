# Definitive Fix for Config Flow Error

## Problem
Getting "500 Internal Server Error" when clicking gear icon, with NO logs appearing.

This means Home Assistant is using cached bytecode and not loading your updated Python files.

## Solution: Force Complete Reload

### Step 1: Remove Integration Completely

1. In Home Assistant, go to **Settings** → **Devices & Services**
2. Find "The Villages Events"
3. Click the three dots → **Delete**
4. Confirm deletion

### Step 2: Clear All Caches (Choose Your Method)

#### Method A: Via SSH/Terminal (Recommended)

```bash
# Stop Home Assistant (if possible)
# Then run:

# Remove Python cache
find /config/custom_components/villages_events -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find /config/custom_components/villages_events -name "*.pyc" -delete 2>/dev/null

# Remove the entire integration folder
rm -rf /config/custom_components/villages_events

# Restart Home Assistant
```

#### Method B: Via Home Assistant OS Terminal Add-on

1. Install "Terminal & SSH" add-on if not installed
2. Open Terminal
3. Run:
```bash
cd /config/custom_components
rm -rf villages_events
```

#### Method C: Via File Editor

1. Install "File Editor" add-on if not installed
2. Navigate to `/config/custom_components/`
3. Delete the `villages_events` folder

### Step 3: Restart Home Assistant

1. Go to **Settings** → **System** → **Restart**
2. Click **Restart Home Assistant**
3. Wait for full restart (2-3 minutes)

### Step 4: Reinstall via HACS

1. Go to **HACS** → **Integrations**
2. Click **⋮** (three dots top right) → **Custom repositories**
3. Add your repository URL
4. Category: **Integration**
5. Click **Add**
6. Find "The Villages Events"
7. Click **Download**
8. Wait for download to complete

### Step 5: Restart Again

1. Go to **Settings** → **System** → **Restart**
2. Click **Restart Home Assistant**
3. Wait for restart

### Step 6: Add Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "The Villages Events"
4. Configure your settings
5. Click **Submit**

### Step 7: Test Options Flow

1. Find "The Villages Events" in Devices & Services
2. Click the **gear icon** (Configure)
3. The options dialog should now open successfully!

## Why This Works

The issue is that Home Assistant caches compiled Python bytecode (`.pyc` files) in `__pycache__` directories. Even when you update the source `.py` files, Home Assistant may continue using the old cached bytecode.

By completely removing the integration folder and reinstalling, you ensure:
1. All old cache files are deleted
2. Fresh Python files are downloaded
3. New bytecode is compiled
4. No stale cache remains

## If It Still Fails

If you still get the error after following all steps:

### Enable Debug Logging

Edit `/config/configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.villages_events: debug
    homeassistant.config_entries: debug
    homeassistant.loader: debug
```

Restart Home Assistant, try opening options, then check logs.

### Check for Syntax Errors

Run Python syntax check:
```bash
python3 -m py_compile /config/custom_components/villages_events/config_flow.py
```

If there's a syntax error, it will show here.

### Verify File Permissions

```bash
ls -la /config/custom_components/villages_events/
```

All files should be readable (start with `-rw-`).

### Last Resort: Manual Installation

1. Download the repository as ZIP from GitHub
2. Extract it
3. Manually copy `custom_components/villages_events/` to `/config/custom_components/`
4. Restart Home Assistant

## Prevention

To avoid this issue in the future:

1. **Always restart Home Assistant** after updating integration files
2. **Clear cache** when updating: `find /config/custom_components/villages_events -name "*.pyc" -delete`
3. **Use HACS redownload** instead of manual file updates

## Summary

The key steps are:
1. ✅ Delete integration in HA
2. ✅ Delete integration folder completely
3. ✅ Restart HA
4. ✅ Reinstall via HACS
5. ✅ Restart HA again
6. ✅ Add integration
7. ✅ Test options flow

This ensures a completely fresh installation with no cached files!
