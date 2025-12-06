# Getting Live Data from The Villages Calendar

Your Home Assistant integration is currently using **mock data** for testing. To fetch real event data from The Villages calendar, you need to install the `python-villages-events` library.

## Quick Start

### Step 1: Install the Library

The library is included in this repository under `python-villages-events/`. Install it:

```bash
cd python-villages-events
pip install .
```

Or if you're using Home Assistant OS, install via SSH or Terminal add-on:

```bash
pip install /config/custom_components/python-villages-events
```

### Step 2: Test the Library

Verify it works:

```bash
cd python-villages-events
python test_library.py
```

You should see real events from The Villages calendar.

### Step 3: Restart Home Assistant

Restart Home Assistant completely (not just reload the integration).

### Step 4: Verify Live Data

Check the logs (**Settings** → **System** → **Logs**):

**Success (Live Data):**
```
Successfully fetched events for 3 venues
```

**Still Mock Data:**
```
python-villages-events library not installed. Using mock data for development/testing.
```

## What's Included

The `python-villages-events` library I created for you includes:

### Files Created:
- `villages_events/__init__.py` - Package initialization
- `villages_events/client.py` - Main VillagesEvents client class
- `villages_events/config.py` - Configuration and URLs
- `villages_events/exceptions.py` - Custom exceptions
- `setup.py` - Package installation configuration
- `README.md` - Library documentation
- `INSTALL.md` - Detailed installation guide
- `test_library.py` - Test script

### Features:
- ✅ Fetches real data from The Villages API
- ✅ Handles authentication automatically
- ✅ Parses events into standardized format
- ✅ Filters by date range
- ✅ Groups events by venue
- ✅ Extracts performer, times, and event details
- ✅ Compatible with Home Assistant's async executor

### Based On:
The library is based on your existing Villages Event Scraper code from:
https://github.com/netnutmike/python-villages-events/tree/V1.1_Preamble

I extracted the core functionality and packaged it as a reusable library.

## Publishing to PyPI (Optional)

To make installation easier for others:

1. **Create PyPI account**: https://pypi.org/account/register/

2. **Install build tools**:
   ```bash
   pip install build twine
   ```

3. **Build the package**:
   ```bash
   cd python-villages-events
   python -m build
   ```

4. **Upload to PyPI**:
   ```bash
   python -m twine upload dist/*
   ```

5. **Update manifest** (already done):
   The integration's `manifest.json` already specifies:
   ```json
   "requirements": ["python-villages-events>=1.1.0"]
   ```

Once published, Home Assistant will automatically install it from PyPI.

## Troubleshooting

### Library Not Found After Installation

**Problem**: Home Assistant still shows "library not installed"

**Solutions**:
1. Ensure you installed in the correct Python environment
2. Check Home Assistant's Python path: `which python3`
3. Try installing with full path: `python3 -m pip install ./python-villages-events`
4. Restart Home Assistant completely (not just reload)

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

- ✅ Integration installed and working with mock data
- ✅ Library created and ready to install
- ⏳ Waiting for library installation
- ⏳ Waiting for live data verification

## Next Steps

1. Install the library (see Step 1 above)
2. Test it works (see Step 2 above)
3. Restart Home Assistant (see Step 3 above)
4. Verify live data (see Step 4 above)
5. (Optional) Publish to PyPI for easier distribution

Once the library is installed, your integration will automatically start fetching real event data from The Villages calendar!
