# python-villages-events

A Python library for fetching entertainment event data from The Villages, Florida calendar API.

## Installation

```bash
pip install python-villages-events
```

Or install from source:

```bash
pip install git+https://github.com/netnutmike/python-villages-events.git
```

## Usage

```python
from villages_events import VillagesEvents
from datetime import date, timedelta

# Create client
client = VillagesEvents()

# Fetch events for today and tomorrow
today = date.today()
tomorrow = today + timedelta(days=1)

events = client.get_events(today, tomorrow)

for event in events:
    print(f"{event['performer']} at {event['venue']}")
    print(f"  Date: {event['date']}")
    print(f"  Time: {event['start_time']} - {event['end_time']}")
    print()
```

## Event Data Structure

Each event dictionary contains:

- `id`: Unique event identifier
- `date`: Event date (date object)
- `venue`: Venue name (string)
- `performer`: Performer/event name (string)
- `start_time`: Start time (datetime object or None)
- `end_time`: End time (datetime object or None)
- `event_type`: Event category/type (string)

## License

GNU General Public License v3.0

## Credits

Based on the Villages Event Scraper by Mike Myers.
