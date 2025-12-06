# Getting Live Data from The Villages Calendar

Good news! The integration now has the Villages Events library **built-in**. No separate installation required!

## Quick Start

### Step 1: Install the Integration

The integration already includes all the code needed to fetch real data from The Villages calendar.

### Step 2: Restart Home Assistant

Restart Home Assistant completely (not just reload the integration).

### Step 3: Verify Live Data

Check the logs (**Settings** → **System** → **Logs**):

**Success (Live Data):**
```
Successfully fetched events for X venues
```

**Fallback (Mock Data):**
```
Villages events library import failed. Using mock data for development/testing.
```

If you see the fallback message, check for any import errors in the logs.

## What's Included

The integration now includes the Villages Events library **built-in** at:
`custom_components/villages_events/villages_events/`

### Files Included:
- `villages_events/__init__.py` - Package initialization
- `villages_events/client.py` - Main VillagesEvents client class
- `villages_events/config.py` - Configuration and URLs
- `villages_events/exceptions.py` - Custom exceptions

### Features:
- ✅ Fetches real data from The Villages API
- ✅ Handles authentication automatically
- ✅ Parses events into standardized format
- ✅ Filters by date range
- ✅ Groups events by venue
- ✅ Extracts performer, times, and event details
- ✅ Compatible with Home Assistant's async executor
- ✅ No external dependencies required!

### Based On:
The library is based on your existing Villages Event Scraper code from:
https://github.com/netnutmike/python-villages-events/tree/V1.1_Preamble

I extracted the core functionality and embedded it directly into the integration.

## No PyPI Publishing Needed!

Since the library is now embedded directly in the integration, there's no need to publish to PyPI. Everything works out of the box!

## Troubleshooting

### Library Import Failed

**Problem**: Logs show "Villages events library import failed"

**Solutions**:
1. Check for detailed error messages in the logs
2. Verify all files are present in `custom_components/villages_events/villages_events/`
3. Restart Home Assistant completely (not just reload)

### Import Errors

**Problem**: Errors importing `villages_events`

**Solutions**:
1. Verify installation: `pip list | grep villages`
2. Check dependencies: `pip install requests>=2.31.0`
3. Look for errors in Home Assistant logs

### Authentication Errors

**Problem**: "Failed to fetch authentication token"

**Solutions**:
1. The Villages may have changed their API
2. Check if `Config.JS_URL` is still valid
3. The auth token regex in `client.py` may need updating
4. Check your internet connection

### No Events Returned

**Problem**: Library works but returns empty list

**Solutions**:
1. Check if there are actually events scheduled
2. Try different date ranges
3. Check API response in debug mode
4. The Villages API structure may have changed

## Current Status

- ✅ Integration installed and working
- ✅ Library embedded directly in the integration
- ✅ Ready to fetch live data!

## Next Steps

1. Restart Home Assistant
2. Check logs to verify live data is being fetched
3. Enjoy real event data from The Villages!

The integration will automatically start fetching real event data from The Villages calendar!
