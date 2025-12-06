# Config Flow Error - FIXED! ✅

## The Problem

Error when clicking gear icon:
```
AttributeError: property 'config_entry' of 'VillagesEventsOptionsFlow' object has no setter
```

## Root Cause

The `OptionsFlow` base class in Home Assistant has `config_entry` as a **read-only property**. We were trying to set it in `__init__`:

```python
# ❌ WRONG - config_entry is read-only
def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
    self.config_entry = config_entry  # This fails!
```

## The Fix

Changed to use a private variable `_config_entry` instead:

```python
# ✅ CORRECT - use a different variable name
def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
    self._config_entry = config_entry  # This works!
```

And updated all references from `self.config_entry` to `self._config_entry`.

## Files Changed

- `custom_components/villages_events/config_flow.py`
  - Line 154: `self._config_entry = config_entry`
  - Line 189: `self._config_entry.data.get(...)`
  - Line 192: `self._config_entry.data.get(...)`
  - Line 225: `self._config_entry.data.get(...)`
  - Line 228: `self._config_entry.data.get(...)`

## How to Apply

### Step 1: Commit and Push
```bash
git add custom_components/villages_events/config_flow.py
git commit -m "Fix config flow: use _config_entry instead of config_entry"
git push origin main
```

### Step 2: Update in Home Assistant

**Via HACS:**
1. Go to **HACS** → **Integrations**
2. Find "The Villages Events"
3. Click **⋮** (three dots) → **Redownload**
4. Wait for download
5. Go to **Settings** → **System** → **Restart**
6. Restart Home Assistant

### Step 3: Test
1. Go to **Settings** → **Devices & Services**
2. Find "The Villages Events"
3. Click the **gear icon** (Configure)
4. ✅ The options dialog should now open!

## Why This Happened

Home Assistant's `OptionsFlow` base class defines `config_entry` as a property that's automatically set by the framework. When we tried to set it manually in `__init__`, Python raised an `AttributeError` because the property has no setter.

The solution is to use a different variable name (like `_config_entry`) for our internal storage.

## Verification

After applying the fix, you should be able to:
- ✅ Click the gear icon without errors
- ✅ See the current settings pre-filled
- ✅ Change update interval
- ✅ Change favorite performers
- ✅ Save changes successfully
- ✅ Integration reloads with new settings

## Additional Notes

This is a common mistake when creating Home Assistant config flows. The base classes have several read-only properties:
- `config_entry` (OptionsFlow)
- `hass` (set by framework)
- `handler` (set by framework)

Always use different variable names (like `_config_entry`) for your own storage to avoid conflicts with framework properties.

## Success!

This was the actual bug causing the 500 error. The fix is simple and the options flow will now work correctly!
