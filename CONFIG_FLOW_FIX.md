# Config Flow Error Fix

## Issue
Getting "Config flow could not be loaded: 500 Internal Server Error" when clicking the gear icon to edit integration settings.

## What Was Fixed

Added comprehensive error handling to the options flow in `config_flow.py`:

### 1. Error Handling in `async_step_init()`
- Wrapped entire method in try-except
- Logs detailed error information
- Returns form with defaults if error occurs
- Shows "unknown" error message to user

### 2. Error Handling in `_get_schema()`
- Safely converts favorite performers list to string
- Handles list, string, or None values
- Falls back to defaults if conversion fails
- Logs errors for debugging

### 3. Added Error Translation
- Added "unknown" error message to strings.json
- Added to translations/en.json
- User-friendly error message displayed

## How to Apply the Fix

### Step 1: Commit and Push Changes
```bash
git add custom_components/villages_events/config_flow.py
git add custom_components/villages_events/strings.json
git add custom_components/villages_events/translations/en.json
git commit -m "Fix config flow error handling"
git push origin main
```

### Step 2: Update in Home Assistant

**Option A: Via HACS (Recommended)**
1. Go to **HACS** → **Integrations**
2. Find "The Villages Events"
3. Click the three dots → **Redownload**
4. Wait for download to complete
5. Go to **Settings** → **System** → **Restart**
6. Restart Home Assistant

**Option B: Manual Update**
1. Delete `/config/custom_components/villages_events/`
2. Copy updated files to `/config/custom_components/villages_events/`
3. Restart Home Assistant

### Step 3: Test the Fix
1. Go to **Settings** → **Devices & Services**
2. Find "The Villages Events"
3. Click the **gear icon** (Configure)
4. The options dialog should now open

If it still fails, check the logs for the detailed error message.

## Checking Logs

If the error persists:

1. Go to **Settings** → **System** → **Logs**
2. Look for errors containing:
   - `villages_events`
   - `config_flow`
   - `Error in options flow`
   - `Error creating options schema`

3. The logs will show the exact error, such as:
   - Data type mismatch
   - Missing configuration keys
   - Invalid data format

## Common Causes

### Cause 1: Invalid Data Type
**Problem:** `favorite_performers` stored as wrong type in config entry

**Fix:** The new code handles list, string, or None values

### Cause 2: Missing Configuration Keys
**Problem:** Config entry missing `update_interval` or `favorite_performers`

**Fix:** Code now uses defaults if keys are missing

### Cause 3: Corrupted Config Entry
**Problem:** Config entry data is corrupted

**Solution:** Remove and re-add the integration

## If Error Still Occurs

### Check Config Entry Data

Enable debug logging in `configuration.yaml`:
```yaml
logger:
  default: warning
  logs:
    custom_components.villages_events: debug
    homeassistant.config_entries: debug
```

Restart Home Assistant and try opening options again. Check logs for detailed error.

### Remove and Re-add Integration

If config entry is corrupted:
1. Go to **Settings** → **Devices & Services**
2. Find "The Villages Events"
3. Click three dots → **Delete**
4. Click **Add Integration**
5. Search for "The Villages Events"
6. Configure with your settings

## What the Fix Does

### Before:
- Options flow crashed on any unexpected data
- No error logging
- Generic 500 error shown to user
- No way to diagnose the issue

### After:
- Gracefully handles unexpected data types
- Logs detailed error information
- Shows user-friendly error message
- Falls back to default values
- Integration remains functional

## Testing

After applying the fix, test:

1. ✅ Opening options dialog (gear icon)
2. ✅ Changing update interval
3. ✅ Changing favorite performers
4. ✅ Saving changes
5. ✅ Integration reloads successfully

All should work without errors!
