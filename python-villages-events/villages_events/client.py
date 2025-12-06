"""Main client for fetching Villages Events data."""

import re
import requests
from datetime import date, datetime
from typing import List, Dict, Any, Optional

from .config import Config
from .exceptions import APIError, AuthError


class VillagesEvents:
    """Client for fetching entertainment events from The Villages."""
    
    def __init__(self, timeout: int = Config.DEFAULT_TIMEOUT):
        """Initialize the Villages Events client.
        
        Args:
            timeout: Request timeout in seconds (default: 10)
        """
        self.timeout = timeout
        self.session = requests.Session()
        self._auth_token: Optional[str] = None
    
    def _fetch_auth_token(self) -> str:
        """Fetch authentication token from The Villages JavaScript file.
        
        Returns:
            Base64 encoded authentication token
            
        Raises:
            AuthError: If token cannot be fetched or parsed
        """
        try:
            response = self.session.get(
                Config.JS_URL,
                headers={'User-Agent': Config.USER_AGENT},
                timeout=self.timeout
            )
            response.raise_for_status()
            
            # Extract token from JavaScript using regex
            # Looking for pattern like: authorization:"Basic <base64_token>"
            match = re.search(r'authorization\s*:\s*["\']Basic\s+([A-Za-z0-9+/=]+)["\']', 
                            response.text)
            
            if not match:
                raise AuthError("Could not find authorization token in JavaScript file")
            
            token = match.group(1)
            return f"Basic {token}"
            
        except requests.exceptions.RequestException as e:
            raise AuthError(f"Failed to fetch authentication token: {e}")
    
    def _get_auth_token(self) -> str:
        """Get cached auth token or fetch a new one.
        
        Returns:
            Authentication token
        """
        if not self._auth_token:
            self._auth_token = self._fetch_auth_token()
        return self._auth_token
    
    def _fetch_events_for_date_range(self, date_range: str) -> List[Dict[str, Any]]:
        """Fetch events for a specific date range.
        
        Args:
            date_range: Date range string ('today', 'tomorrow', etc.)
            
        Returns:
            List of event dictionaries
            
        Raises:
            APIError: If API request fails
        """
        auth_token = self._get_auth_token()
        api_url = Config.get_api_url(date_range)
        
        headers = {
            'Authorization': auth_token,
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': Config.USER_AGENT,
            'Origin': 'https://www.thevillages.com',
            'Referer': Config.CALENDAR_BASE_URL,
        }
        
        try:
            response = self.session.get(api_url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            if not isinstance(data, dict):
                raise APIError(f"Invalid API response: expected dict, got {type(data).__name__}")
            
            # Extract events from response
            # The API returns data in format: {"data": [...], "totalRows": N}
            events = data.get('data', [])
            
            if not isinstance(events, list):
                raise APIError(f"Invalid events data: expected list, got {type(events).__name__}")
            
            return events
            
        except requests.exceptions.RequestException as e:
            raise APIError(f"API request failed: {e}")
        except ValueError as e:
            raise APIError(f"Failed to parse JSON response: {e}")
    
    def get_events(self, start_date: date, end_date: date) -> List[Dict[str, Any]]:
        """Fetch events between start_date and end_date.
        
        Args:
            start_date: Start date for events
            end_date: End date for events
            
        Returns:
            List of event dictionaries with standardized format:
            {
                "date": date object,
                "venue": str,
                "performer": str,
                "start_time": datetime or None,
                "end_time": datetime or None,
                "event_type": str
            }
        """
        all_events = []
        today = date.today()
        
        # Determine which date ranges to fetch
        date_ranges = []
        if start_date <= today <= end_date:
            date_ranges.append('today')
        if start_date <= (today + timedelta(days=1)) <= end_date:
            date_ranges.append('tomorrow')
        
        # If no specific ranges match, fetch this-week
        if not date_ranges:
            date_ranges.append('this-week')
        
        # Fetch events for each date range
        for date_range in date_ranges:
            raw_events = self._fetch_events_for_date_range(date_range)
            
            # Process and filter events
            for event in raw_events:
                processed_event = self._process_event(event, start_date, end_date)
                if processed_event:
                    all_events.append(processed_event)
        
        # Remove duplicates based on event ID
        seen_ids = set()
        unique_events = []
        for event in all_events:
            event_id = event.get('id')
            if event_id and event_id not in seen_ids:
                seen_ids.add(event_id)
                unique_events.append(event)
        
        return unique_events
    
    def _process_event(self, event: Dict[str, Any], start_date: date, 
                      end_date: date) -> Optional[Dict[str, Any]]:
        """Process raw API event into standardized format.
        
        Args:
            event: Raw event data from API
            start_date: Filter start date
            end_date: Filter end date
            
        Returns:
            Processed event dictionary or None if event should be filtered out
        """
        try:
            # Extract event date
            start_info = event.get('start', {})
            event_date_str = start_info.get('date')
            
            if not event_date_str:
                return None
            
            # Parse date (format: YYYY-MM-DD)
            event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
            
            # Filter by date range
            if not (start_date <= event_date <= end_date):
                return None
            
            # Extract location/venue
            location = event.get('location', {})
            venue = location.get('title', 'Unknown Venue')
            
            # Extract performer/title
            performer = event.get('title', 'Unknown')
            
            # Extract times
            start_time = None
            end_time = None
            
            if not event.get('allDay', False):
                start_time_str = start_info.get('time')
                if start_time_str:
                    try:
                        start_time = datetime.strptime(
                            f"{event_date_str} {start_time_str}",
                            '%Y-%m-%d %H:%M:%S'
                        )
                    except ValueError:
                        pass
                
                end_info = event.get('end', {})
                end_time_str = end_info.get('time')
                if end_time_str:
                    try:
                        end_time = datetime.strptime(
                            f"{event_date_str} {end_time_str}",
                            '%Y-%m-%d %H:%M:%S'
                        )
                    except ValueError:
                        pass
            
            # Extract event type/category
            category = event.get('category', 'Event')
            
            return {
                'id': event.get('id'),
                'date': event_date,
                'venue': venue,
                'performer': performer,
                'start_time': start_time,
                'end_time': end_time,
                'event_type': category,
            }
            
        except (KeyError, ValueError, TypeError):
            # Skip events with invalid data
            return None


# Import timedelta for date calculations
from datetime import timedelta
