import os
import requests
from typing import Dict, List, Any, Optional
from config.logger import log


class YelpClient:
    """Yelp API client for business search and reviews."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('YELP_API_KEY')
        self.base_url = "https://api.yelp.com/v3"
        
        if not self.api_key:
            log.warning("Yelp API key not found. Set YELP_API_KEY environment variable.")
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        log.info("Yelp client initialized")
    
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Make a request to the Yelp API."""
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            log.error(f"Yelp API request failed: {e}")
            return None
        except Exception as e:
            log.error(f"Yelp request error: {e}")
            return None
    
    def search_businesses(self, location: str, term: str = None, categories: str = None, 
                         radius: int = 40000, limit: int = 20, offset: int = 0) -> Optional[List[Dict[str, Any]]]:
        """Search for businesses on Yelp."""
        try:
            params = {
                'location': location,
                'radius': radius,
                'limit': limit,
                'offset': offset
            }
            
            if term:
                params['term'] = term
            if categories:
                params['categories'] = categories
            
            response = self._make_request('businesses/search', params)
            
            if response and 'businesses' in response:
                businesses = response['businesses']
                log.info(f"Found {len(businesses)} businesses in {location}")
                return businesses
            else:
                log.error(f"Business search failed: {response}")
                return None
                
        except Exception as e:
            log.error(f"Business search error: {e}")
            return None
    
    def get_business_details(self, business_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific business."""
        try:
            response = self._make_request(f'businesses/{business_id}')
            
            if response:
                log.info(f"Retrieved details for business: {response.get('name', 'Unknown')}")
                return response
            else:
                log.error(f"Failed to get business details for {business_id}")
                return None
                
        except Exception as e:
            log.error(f"Get business details error: {e}")
            return None
    
    def get_business_reviews(self, business_id: str, limit: int = 20) -> Optional[List[Dict[str, Any]]]:
        """Get reviews for a specific business."""
        try:
            params = {'limit': limit}
            response = self._make_request(f'businesses/{business_id}/reviews', params)
            
            if response and 'reviews' in response:
                reviews = response['reviews']
                log.info(f"Retrieved {len(reviews)} reviews for business {business_id}")
                return reviews
            else:
                log.error(f"Failed to get reviews for {business_id}")
                return None
                
        except Exception as e:
            log.error(f"Get reviews error: {e}")
            return None
    
    def search_restaurants(self, location: str, cuisine: str = None, price: str = None, 
                          radius: int = 40000, limit: int = 20) -> Optional[List[Dict[str, Any]]]:
        """Search specifically for restaurants."""
        try:
            categories = "restaurants"
            if cuisine:
                categories += f",{cuisine}"
            
            return self.search_businesses(
                location=location,
                categories=categories,
                radius=radius,
                limit=limit
            )
            
        except Exception as e:
            log.error(f"Restaurant search error: {e}")
            return None
    
    def search_hotels(self, location: str, radius: int = 40000, limit: int = 20) -> Optional[List[Dict[str, Any]]]:
        """Search specifically for hotels."""
        try:
            return self.search_businesses(
                location=location,
                categories="hotels",
                radius=radius,
                limit=limit
            )
            
        except Exception as e:
            log.error(f"Hotel search error: {e}")
            return None
    
    def search_activities(self, location: str, activity_type: str = None, 
                         radius: int = 40000, limit: int = 20) -> Optional[List[Dict[str, Any]]]:
        """Search for activities and attractions."""
        try:
            categories = "active,arts,beautysvc,education,health,localflavor,nightlife,shopping"
            if activity_type:
                categories += f",{activity_type}"
            
            return self.search_businesses(
                location=location,
                categories=categories,
                radius=radius,
                limit=limit
            )
            
        except Exception as e:
            log.error(f"Activity search error: {e}")
            return None
    
    def search_nearby(self, latitude: float, longitude: float, term: str = None, 
                      radius: int = 40000, limit: int = 20) -> Optional[List[Dict[str, Any]]]:
        """Search for businesses near specific coordinates."""
        try:
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'radius': radius,
                'limit': limit
            }
            
            if term:
                params['term'] = term
            
            response = self._make_request('businesses/search', params)
            
            if response and 'businesses' in response:
                businesses = response['businesses']
                log.info(f"Found {len(businesses)} businesses near ({latitude}, {longitude})")
                return businesses
            else:
                log.error(f"Nearby search failed: {response}")
                return None
                
        except Exception as e:
            log.error(f"Nearby search error: {e}")
            return None
    
    def get_business_hours(self, business_id: str) -> Optional[Dict[str, Any]]:
        """Get business hours for a specific business."""
        try:
            business = self.get_business_details(business_id)
            
            if business and 'hours' in business:
                hours = business['hours']
                log.info(f"Retrieved hours for business {business_id}")
                return hours
            else:
                log.warning(f"No hours available for business {business_id}")
                return None
                
        except Exception as e:
            log.error(f"Get business hours error: {e}")
            return None
    
    def search_by_phone(self, phone: str) -> Optional[Dict[str, Any]]:
        """Search for a business by phone number."""
        try:
            params = {'phone': phone}
            response = self._make_request('businesses/search/phone', params)
            
            if response and 'businesses' in response and response['businesses']:
                business = response['businesses'][0]
                log.info(f"Found business by phone: {business.get('name', 'Unknown')}")
                return business
            else:
                log.warning(f"No business found for phone number: {phone}")
                return None
                
        except Exception as e:
            log.error(f"Phone search error: {e}")
            return None
    
    def get_autocomplete(self, text: str, latitude: float = None, longitude: float = None) -> Optional[List[Dict[str, Any]]]:
        """Get autocomplete suggestions for business names."""
        try:
            params = {'text': text}
            
            if latitude and longitude:
                params['latitude'] = latitude
                params['longitude'] = longitude
            
            response = self._make_request('autocomplete', params)
            
            if response and 'terms' in response:
                suggestions = response['terms']
                log.info(f"Retrieved {len(suggestions)} autocomplete suggestions")
                return suggestions
            else:
                log.error(f"Autocomplete failed: {response}")
                return None
                
        except Exception as e:
            log.error(f"Autocomplete error: {e}")
            return None
    
    def get_business_photos(self, business_id: str) -> Optional[List[str]]:
        """Get photo URLs for a business."""
        try:
            business = self.get_business_details(business_id)
            
            if business and 'photos' in business:
                photos = business['photos']
                log.info(f"Retrieved {len(photos)} photos for business {business_id}")
                return photos
            else:
                log.warning(f"No photos available for business {business_id}")
                return None
                
        except Exception as e:
            log.error(f"Get business photos error: {e}")
            return None 