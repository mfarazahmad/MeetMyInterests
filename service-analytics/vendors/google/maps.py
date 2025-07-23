import os
import requests
from typing import Dict, List, Any, Optional, Tuple
from config.logger import log


class GoogleMapsClient:
    """Google Maps API client with geocoding, directions, and places functionality."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('GOOGLE_MAPS_API_KEY')
        self.base_url = "https://maps.googleapis.com/maps/api"
        
        if not self.api_key:
            log.warning("Google Maps API key not found. Set GOOGLE_MAPS_API_KEY environment variable.")
        
        log.info("Google Maps client initialized")
    
    def geocode(self, address: str) -> Optional[Dict[str, Any]]:
        """Convert address to coordinates."""
        try:
            url = f"{self.base_url}/geocode/json"
            params = {
                'address': address,
                'key': self.api_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if data['status'] == 'OK':
                result = data['results'][0]
                location = result['geometry']['location']
                log.info(f"Geocoded '{address}' to {location}")
                return {
                    'lat': location['lat'],
                    'lng': location['lng'],
                    'formatted_address': result['formatted_address'],
                    'place_id': result['place_id']
                }
            else:
                log.error(f"Geocoding failed for '{address}': {data['status']}")
                return None
                
        except Exception as e:
            log.error(f"Geocoding error for '{address}': {e}")
            return None
    
    def reverse_geocode(self, lat: float, lng: float) -> Optional[Dict[str, Any]]:
        """Convert coordinates to address."""
        try:
            url = f"{self.base_url}/geocode/json"
            params = {
                'latlng': f"{lat},{lng}",
                'key': self.api_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if data['status'] == 'OK':
                result = data['results'][0]
                log.info(f"Reverse geocoded ({lat}, {lng}) to '{result['formatted_address']}'")
                return {
                    'formatted_address': result['formatted_address'],
                    'place_id': result['place_id'],
                    'components': result.get('address_components', [])
                }
            else:
                log.error(f"Reverse geocoding failed for ({lat}, {lng}): {data['status']}")
                return None
                
        except Exception as e:
            log.error(f"Reverse geocoding error for ({lat}, {lng}): {e}")
            return None
    
    def get_directions(self, origin: str, destination: str, mode: str = "driving") -> Optional[Dict[str, Any]]:
        """Get directions between two points."""
        try:
            url = f"{self.base_url}/directions/json"
            params = {
                'origin': origin,
                'destination': destination,
                'mode': mode,
                'key': self.api_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if data['status'] == 'OK':
                route = data['routes'][0]
                leg = route['legs'][0]
                
                directions = {
                    'distance': leg['distance']['text'],
                    'duration': leg['duration']['text'],
                    'start_address': leg['start_address'],
                    'end_address': leg['end_address'],
                    'steps': [step['html_instructions'] for step in leg['steps']]
                }
                
                log.info(f"Got directions from '{origin}' to '{destination}': {directions['distance']}, {directions['duration']}")
                return directions
            else:
                log.error(f"Directions failed: {data['status']}")
                return None
                
        except Exception as e:
            log.error(f"Directions error: {e}")
            return None
    
    def search_places(self, query: str, location: str = None, radius: int = 5000) -> Optional[List[Dict[str, Any]]]:
        """Search for places using Google Places API."""
        try:
            url = f"{self.base_url}/place/textsearch/json"
            params = {
                'query': query,
                'key': self.api_key
            }
            
            if location:
                # Geocode the location first
                geocode_result = self.geocode(location)
                if geocode_result:
                    params['location'] = f"{geocode_result['lat']},{geocode_result['lng']}"
                    params['radius'] = radius
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if data['status'] == 'OK':
                places = []
                for place in data['results']:
                    places.append({
                        'name': place['name'],
                        'place_id': place['place_id'],
                        'formatted_address': place.get('formatted_address', ''),
                        'rating': place.get('rating', 0),
                        'types': place.get('types', []),
                        'geometry': place['geometry']
                    })
                
                log.info(f"Found {len(places)} places for query: '{query}'")
                return places
            else:
                log.error(f"Places search failed: {data['status']}")
                return None
                
        except Exception as e:
            log.error(f"Places search error: {e}")
            return None
    
    def get_place_details(self, place_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a place."""
        try:
            url = f"{self.base_url}/place/details/json"
            params = {
                'place_id': place_id,
                'fields': 'name,formatted_address,geometry,rating,reviews,opening_hours,website,formatted_phone_number',
                'key': self.api_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if data['status'] == 'OK':
                place = data['result']
                log.info(f"Retrieved details for place: {place['name']}")
                return place
            else:
                log.error(f"Place details failed: {data['status']}")
                return None
                
        except Exception as e:
            log.error(f"Place details error: {e}")
            return None
    
    def calculate_distance(self, origin: str, destination: str, mode: str = "driving") -> Optional[Dict[str, Any]]:
        """Calculate distance and travel time between two points."""
        try:
            directions = self.get_directions(origin, destination, mode)
            if directions:
                return {
                    'distance': directions['distance'],
                    'duration': directions['duration'],
                    'mode': mode
                }
            return None
            
        except Exception as e:
            log.error(f"Distance calculation error: {e}")
            return None
    
    def get_nearby_places(self, location: str, radius: int = 5000, place_type: str = None) -> Optional[List[Dict[str, Any]]]:
        """Get nearby places around a location."""
        try:
            # Geocode the location first
            geocode_result = self.geocode(location)
            if not geocode_result:
                return None
            
            url = f"{self.base_url}/place/nearbysearch/json"
            params = {
                'location': f"{geocode_result['lat']},{geocode_result['lng']}",
                'radius': radius,
                'key': self.api_key
            }
            
            if place_type:
                params['type'] = place_type
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if data['status'] == 'OK':
                places = []
                for place in data['results']:
                    places.append({
                        'name': place['name'],
                        'place_id': place['place_id'],
                        'rating': place.get('rating', 0),
                        'types': place.get('types', []),
                        'vicinity': place.get('vicinity', ''),
                        'geometry': place['geometry']
                    })
                
                log.info(f"Found {len(places)} nearby places around '{location}'")
                return places
            else:
                log.error(f"Nearby places search failed: {data['status']}")
                return None
                
        except Exception as e:
            log.error(f"Nearby places error: {e}")
            return None
