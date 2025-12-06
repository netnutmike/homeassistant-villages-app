"""Configuration constants for Villages Events library."""


class Config:
    """Configuration constants."""
    
    # URLs
    JS_URL = "https://cdn.thevillages.com/web_components/myvillages-auth-forms/main.js"
    CALENDAR_BASE_URL = "https://www.thevillages.com/calendar/"
    API_BASE_URL = "https://api.v2.thevillages.com/events/"
    
    # HTTP settings
    DEFAULT_TIMEOUT = 10
    USER_AGENT = "Mozilla/5.0 (compatible; HomeAssistant/1.0)"
    
    # API parameters
    DEFAULT_CATEGORY = "entertainment"
    DEFAULT_LOCATION = "town-squares"
    
    @staticmethod
    def get_api_url(date_range: str, category: str = DEFAULT_CATEGORY, 
                    location: str = DEFAULT_LOCATION) -> str:
        """Generate API URL with filters.
        
        Args:
            date_range: Date range (e.g., 'today', 'tomorrow', 'this-week')
            category: Event category (default: 'entertainment')
            location: Location filter (default: 'town-squares')
            
        Returns:
            Complete API URL with query parameters
        """
        params = [
            "cancelled=false",
            "startRow=0",
            "endRow=100",  # Fetch more events
            f"dateRange={date_range}",
            f"categories={category}",
            f"locationCategories={location}",
            "subcategoriesQueryType=and"
        ]
        return Config.API_BASE_URL + "?" + "&".join(params)
