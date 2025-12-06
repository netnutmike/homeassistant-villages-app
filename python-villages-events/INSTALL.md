# Installation Guide for python-villages-events

This library needs to be installed for the Home Assistant integration to fetch real data.

## Option 1: Install from Local Directory (For Testing)

If you're developing locally:

```bash
cd python-villages-events
pip install -e .
```

Or from your Home Assistant environment:

```bash
# SSH into Home Assistant or use the Terminal add-on
pip install /path/to/python-villages-events
```

## Option 2: Install from GitHub (Temporary)

Until the package is published to PyPI:

```bash
pip install git+https://github.com/yourusername/python-villages-events.git
```

## Option 3: Publish to PyPI (Recommended for Production)

1. **Create PyPI account** at https://pypi.org/account/register/

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

5. **Update manifest.json** (already done):
   ```json
   "requirements": ["python-villages-events>=1.1.0"]
   ```

6. **Restart Home Assistant** - it will automatically install from PyPI

## Verify Installation

Test that the library works:

```python
from villages_events import VillagesEvents
from datetime import date, timedelta

client = VillagesEvents()
today = date.today()
tomorrow = today + timedelta(days=1)

events = client.get_events(today, tomorrow)
print(f"Found {len(events)} events")
for event in events[:3]:  # Show first 3
    print(f"- {event['performer']} at {event['venue']}")
```

## For Home Assistant Integration

Once the library is installed (via any method above):

1. **Restart Home Assistant** completely
2. The integration will automatically detect the library
3. Check logs - you should see:
   ```
   Successfully fetched events for X venues
   ```
   Instead of:
   ```
   Using mock data for development/testing
   ```

## Troubleshooting

### Library Not Found

If Home Assistant can't find the library:

1. Check it's installed in the correct Python environment
2. Try manual installation via SSH/Terminal
3. Check Home Assistant logs for import errors

### Import Errors

If you see import errors, ensure all dependencies are installed:

```bash
pip install requests>=2.31.0
```

### Authentication Errors

If you see authentication errors:
- The Villages may have changed their API
- Check if the JS_URL in config.py is still valid
- The auth token extraction regex may need updating
