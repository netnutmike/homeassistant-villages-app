#!/usr/bin/env python3
"""Test script for python-villages-events library."""

from datetime import date, timedelta
from villages_events import VillagesEvents

def main():
    """Test the Villages Events library."""
    print("Testing python-villages-events library...")
    print("-" * 50)
    
    # Create client
    client = VillagesEvents()
    
    # Fetch events for today and tomorrow
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    print(f"Fetching events from {today} to {tomorrow}...")
    
    try:
        events = client.get_events(today, tomorrow)
        
        print(f"\nFound {len(events)} events\n")
        
        # Group by venue
        venues = {}
        for event in events:
            venue = event['venue']
            if venue not in venues:
                venues[venue] = []
            venues[venue].append(event)
        
        # Display events by venue
        for venue, venue_events in venues.items():
            print(f"\n{venue} ({len(venue_events)} events):")
            print("-" * 50)
            for event in venue_events:
                print(f"  {event['performer']}")
                print(f"    Date: {event['date']}")
                if event['start_time']:
                    print(f"    Time: {event['start_time'].strftime('%I:%M %p')} - {event['end_time'].strftime('%I:%M %p') if event['end_time'] else 'N/A'}")
                print(f"    Type: {event['event_type']}")
                print()
        
        print("\n✓ Library test successful!")
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
