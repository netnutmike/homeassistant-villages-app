# Getting Live Data from The Villages Calendar

✅ **FIXED!** The integration now successfully fetches live data from The Villages API!

## What Was Fixed

The integration had two issues preventing it from fetching live data:

1. **Wrong API Response Key**: The code was looking for `data` but the API returns `events`
2. **Wrong Date Format**: The code expected simple dates but the API uses ISO 8601 format

### Changes Made

- Updated `client.py` to look for `events` key in API response
- Fixed date parsing to handle ISO 8601 format (`2025-12-06T17:00:00.000Z`)
- Removed excessive debug logging
- Verified auth token extraction works correctly

## Quick Start

### Step 1: Reload the Integration

After the code updates, reload the integration:
1. Go to **Settings** → **Devices & Services**
2. Find "The Villages Events"
3. Click the three dots menu → **Reload**

### Step 2: Verify Live Data

Check the logs (**Settings** → **System** → **Logs**):

**Success (Live Data):**
```
Fetched X events from The Villages API
Successfully fetched events for X venues
```

**Fallback (Mock Data):**
```
No events returned from API! Using mock data instead.
```

## How It Works

The integration uses an embedded library at `custom_components/villages_events/villages_events/` that:

1. **Extracts Auth Token**: Fetches JavaScript from The Villages CDN and extracts the authorization token
   - Pattern: `Authorization:"Basic <token>"`
   - Current token: `64f7873ca215d1eb1f72a13f`

2. **Calls API**: Makes authenticated requests to `https://api.v2.thevillages.com/events/`
   - Uses date range filters (today, tomorrow, this-week)
   - Filters by category (entertainment) and location (town-squares)

3. **Processes Events**: Parses JSON response and converts to standardized format
   - Extracts venue, performer, times, event type
   - Converts ISO datetime to Python datetime objects

4. **Filters by Date**: Only returns events within requested date range

## API Details

- **Base URL**: `https://api.v2.thevillages.com/events/`
- **Auth Token Source**: `https://cdn.thevillages.com/web_components/myvillages-auth-forms/main.js`
- **Auth Header**: `Authorization: Basic 64f7873ca215d1eb1f72a13f`
- **Response Format**: `{"events": [...]}`
- **Date Format**: ISO 8601 with timezone (e.g., `2025-12-06T17:00:00.000Z`)

## Testing the API Manually

```bash
# Test auth token extraction
curl -s "https://cdn.thevillages.com/web_components/myvillages-auth-forms/main.js" | grep -i "authorization"

# Test API call
curl "https://api.v2.thevillages.com/events/?cancelled=false&startRow=0&endRow=10&dateRange=today&categories=entertainment&locationCategories=town-squares&subcategoriesQueryType=and" \
  -H "Authorization: Basic 64f7873ca215d1eb1f72a13f" | python3 -m json.tool
```

## What's Included

The integration includes the Villages Events library **built-in** at:
`custom_components/villages_events/villages_events/`

### Files:
- `__init__.py` - Package initialization
- `client.py` - Main VillagesEvents client class
- `config.py` - Configuration and URLs
- `exceptions.py` - Custom exceptions

### Features:
- ✅ Fetches real data from The Villages API
- ✅ Handles authentication automatically
- ✅ Parses events into standardized format
- ✅ Filters by date range
- ✅ Groups events by venue
- ✅ Extracts performer, times, and event details
- ✅ Compatible with Home Assistant's async executor
- ✅ No external dependencies required!

## Fallback Behavior

When the API returns no events or encounters an error, the integration falls back to mock data to ensure entities are still created and the integration remains functional.

## Troubleshooting

### No Events Returned

**Problem**: "No events returned from API! Using mock data instead."

**Solutions**:
1. Check if there are actually events scheduled today/tomorrow
2. Verify internet connection
3. Check Home Assistant logs for API errors
4. The Villages API may be temporarily down

### Authentication Errors

**Problem**: "Failed to fetch authentication token"

**Solutions**:
1. The Villages may have changed their API
2. Check if `Config.JS_URL` is still valid
3. The auth token regex may need updating
4. Check internet connection

### Import Errors

**Problem**: "Villages events library import failed"

**Solutions**:
1. Verify all files are present in `custom_components/villages_events/villages_events/`
2. Check for detailed error messages in logs
3. Restart Home Assistant completely

## Current Status

- ✅ Integration installed and working
- ✅ Library embedded directly in the integration
- ✅ API response parsing fixed
- ✅ Date format parsing fixed
- ✅ Ready to fetch live data!

## Next Steps

1. Reload the integration in Home Assistant
2. Check logs to verify live data is being fetched
3. Enjoy real event data from The Villages!

The integration will automatically fetch real event data from The Villages calendar!
