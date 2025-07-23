import os
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from config.logger import log


class SkyscannerClient:
    """Skyscanner API client for flight search and booking."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('SKYSCANNER_API_KEY')
        self.base_url = "https://partners.api.skyscanner.net/apiservices"
        
        if not self.api_key:
            log.warning("Skyscanner API key not found. Set SKYSCANNER_API_KEY environment variable.")
        
        self.headers = {
            'Accept': 'application/json',
            'X-API-Key': self.api_key
        }
        
        log.info("Skyscanner client initialized")
    
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Make a request to the Skyscanner API."""
        try:
            url = f"{self.base_url}/{endpoint}"
            
            if not params:
                params = {}
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            log.error(f"Skyscanner API request failed: {e}")
            return None
        except Exception as e:
            log.error(f"Skyscanner request error: {e}")
            return None
    
    def browse_quotes(self, origin: str, destination: str, outbound_date: str, 
                      inbound_date: str = None, currency: str = "USD", 
                      locale: str = "en-US", country: str = "US") -> Optional[Dict[str, Any]]:
        """Browse flight quotes for a route."""
        try:
            params = {
                'originplace': f"{origin}-sky",
                'destinationplace': f"{destination}-sky",
                'outbounddate': outbound_date,
                'currency': currency,
                'locale': locale,
                'country': country
            }
            
            if inbound_date:
                params['inbounddate'] = inbound_date
            
            response = self._make_request('browsequotes/v1.0', params)
            
            if response:
                log.info(f"Retrieved flight quotes from {origin} to {destination} on {outbound_date}")
                return response
            else:
                log.error(f"Failed to get flight quotes from {origin} to {destination}")
                return None
                
        except Exception as e:
            log.error(f"Browse quotes error: {e}")
            return None
    
    def browse_routes(self, origin: str, destination: str, outbound_date: str,
                      inbound_date: str = None, currency: str = "USD",
                      locale: str = "en-US", country: str = "US") -> Optional[Dict[str, Any]]:
        """Browse flight routes for a journey."""
        try:
            params = {
                'originplace': f"{origin}-sky",
                'destinationplace': f"{destination}-sky",
                'outbounddate': outbound_date,
                'currency': currency,
                'locale': locale,
                'country': country
            }
            
            if inbound_date:
                params['inbounddate'] = inbound_date
            
            response = self._make_request('browseroutes/v1.0', params)
            
            if response:
                log.info(f"Retrieved flight routes from {origin} to {destination}")
                return response
            else:
                log.error(f"Failed to get flight routes from {origin} to {destination}")
                return None
                
        except Exception as e:
            log.error(f"Browse routes error: {e}")
            return None
    
    def browse_dates(self, origin: str, destination: str, currency: str = "USD",
                     locale: str = "en-US", country: str = "US") -> Optional[Dict[str, Any]]:
        """Browse flight dates for a route."""
        try:
            params = {
                'originplace': f"{origin}-sky",
                'destinationplace': f"{destination}-sky",
                'currency': currency,
                'locale': locale,
                'country': country
            }
            
            response = self._make_request('browsedates/v1.0', params)
            
            if response:
                log.info(f"Retrieved flight dates from {origin} to {destination}")
                return response
            else:
                log.error(f"Failed to get flight dates from {origin} to {destination}")
                return None
                
        except Exception as e:
            log.error(f"Browse dates error: {e}")
            return None
    
    def get_places(self, query: str, country: str = "US", currency: str = "USD",
                   locale: str = "en-US") -> Optional[List[Dict[str, Any]]]:
        """Search for places (airports, cities, etc.)."""
        try:
            params = {
                'query': query,
                'country': country,
                'currency': currency,
                'locale': locale
            }
            
            response = self._make_request('autosuggest/v1.0', params)
            
            if response and 'Places' in response:
                places = response['Places']
                log.info(f"Found {len(places)} places matching '{query}'")
                return places
            else:
                log.warning(f"No places found for '{query}'")
                return []
                
        except Exception as e:
            log.error(f"Get places error: {e}")
            return None
    
    def get_geo_hierarchy(self, country: str = "US", currency: str = "USD",
                          locale: str = "en-US") -> Optional[Dict[str, Any]]:
        """Get geographical hierarchy for a country."""
        try:
            params = {
                'country': country,
                'currency': currency,
                'locale': locale
            }
            
            response = self._make_request('geo/v1.0', params)
            
            if response:
                log.info(f"Retrieved geo hierarchy for {country}")
                return response
            else:
                log.error(f"Failed to get geo hierarchy for {country}")
                return None
                
        except Exception as e:
            log.error(f"Get geo hierarchy error: {e}")
            return None
    
    def get_carriers(self, country: str = "US", currency: str = "USD",
                     locale: str = "en-US") -> Optional[List[Dict[str, Any]]]:
        """Get list of carriers (airlines)."""
        try:
            params = {
                'country': country,
                'currency': currency,
                'locale': locale
            }
            
            response = self._make_request('reference/v1.0/carriers', params)
            
            if response and 'Carriers' in response:
                carriers = response['Carriers']
                log.info(f"Retrieved {len(carriers)} carriers")
                return carriers
            else:
                log.error("Failed to get carriers")
                return None
                
        except Exception as e:
            log.error(f"Get carriers error: {e}")
            return None
    
    def get_currencies(self, locale: str = "en-US") -> Optional[List[Dict[str, Any]]]:
        """Get list of supported currencies."""
        try:
            params = {'locale': locale}
            
            response = self._make_request('reference/v1.0/currencies', params)
            
            if response and 'Currencies' in response:
                currencies = response['Currencies']
                log.info(f"Retrieved {len(currencies)} currencies")
                return currencies
            else:
                log.error("Failed to get currencies")
                return None
                
        except Exception as e:
            log.error(f"Get currencies error: {e}")
            return None
    
    def get_places_by_id(self, place_id: str, country: str = "US", currency: str = "USD",
                         locale: str = "en-US") -> Optional[Dict[str, Any]]:
        """Get place details by ID."""
        try:
            params = {
                'country': country,
                'currency': currency,
                'locale': locale
            }
            
            response = self._make_request(f'reference/v1.0/places/{place_id}', params)
            
            if response:
                log.info(f"Retrieved place details for {place_id}")
                return response
            else:
                log.error(f"Failed to get place details for {place_id}")
                return None
                
        except Exception as e:
            log.error(f"Get place by ID error: {e}")
            return None
    
    def get_cheapest_quotes(self, origin: str, destination: str, outbound_date: str,
                            inbound_date: str = None, currency: str = "USD",
                            locale: str = "en-US", country: str = "US") -> Optional[List[Dict[str, Any]]]:
        """Get the cheapest flight quotes for a route."""
        try:
            quotes_response = self.browse_quotes(
                origin=origin,
                destination=destination,
                outbound_date=outbound_date,
                inbound_date=inbound_date,
                currency=currency,
                locale=locale,
                country=country
            )
            
            if quotes_response and 'Quotes' in quotes_response:
                quotes = quotes_response['Quotes']
                
                # Sort by price (MinPrice)
                cheapest_quotes = sorted(quotes, key=lambda x: x.get('MinPrice', float('inf')))
                
                log.info(f"Found {len(cheapest_quotes)} quotes, cheapest: ${cheapest_quotes[0].get('MinPrice', 0)}")
                return cheapest_quotes
            else:
                log.warning(f"No quotes found for {origin} to {destination}")
                return []
                
        except Exception as e:
            log.error(f"Get cheapest quotes error: {e}")
            return None
    
    def search_flights(self, origin: str, destination: str, departure_date: str,
                       return_date: str = None, adults: int = 1, children: int = 0,
                       infants: int = 0, cabin_class: str = "economy") -> Optional[Dict[str, Any]]:
        """Search for flights with specific parameters."""
        try:
            # Format dates
            if isinstance(departure_date, datetime):
                departure_date = departure_date.strftime('%Y-%m-%d')
            if return_date and isinstance(return_date, datetime):
                return_date = return_date.strftime('%Y-%m-%d')
            
            quotes_response = self.browse_quotes(
                origin=origin,
                destination=destination,
                outbound_date=departure_date,
                inbound_date=return_date
            )
            
            if quotes_response:
                # Add passenger and cabin information
                search_results = {
                    'origin': origin,
                    'destination': destination,
                    'departure_date': departure_date,
                    'return_date': return_date,
                    'passengers': {
                        'adults': adults,
                        'children': children,
                        'infants': infants
                    },
                    'cabin_class': cabin_class,
                    'quotes': quotes_response.get('Quotes', []),
                    'places': quotes_response.get('Places', []),
                    'carriers': quotes_response.get('Carriers', [])
                }
                
                log.info(f"Flight search completed: {origin} to {destination}")
                return search_results
            else:
                log.error(f"Flight search failed: {origin} to {destination}")
                return None
                
        except Exception as e:
            log.error(f"Search flights error: {e}")
            return None
    
    def get_flight_details(self, quote_id: str, country: str = "US", currency: str = "USD",
                          locale: str = "en-US") -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific flight quote."""
        try:
            params = {
                'country': country,
                'currency': currency,
                'locale': locale
            }
            
            response = self._make_request(f'pricing/v1.0/{quote_id}', params)
            
            if response:
                log.info(f"Retrieved flight details for quote {quote_id}")
                return response
            else:
                log.error(f"Failed to get flight details for quote {quote_id}")
                return None
                
        except Exception as e:
            log.error(f"Get flight details error: {e}")
            return None 