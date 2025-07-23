import os
import spacy
from dateutil.parser import parse as parse_date
from typing import List, Dict, Any, Tuple

from ai.utils import embedding_generator
from config.bootstrap import vectorIndex, yelp_client, weather_client, skyscanner_client

nlp = spacy.load("en_core_web_sm")

def initialize_trip_index(location: str) -> None:
    """Initialize trip index with location data."""
    types = ['restaurants', 'activities', 'hotels', 'hospitals']
    for term in types:
        data = fetch_yelp_data(location, term)
        if data:
            contexts = preprocess_trip_contexts(data)
            encode_and_store_trip_contexts(contexts, namespace='trips')

def fetch_yelp_data(location: str, term: str) -> Dict[str, Any]:
    """Fetch Yelp data using the new Yelp client."""
    try:
        if not yelp_client:
            print("Yelp client not initialized")
            return {}
        
        businesses = yelp_client.search_businesses(
            location=location,
            term=term,
            limit=5
        )
        
        return {'businesses': businesses} if businesses else {}
        
    except Exception as e:
        print(f"Error fetching Yelp data: {e}")
        return {}

def preprocess_trip_contexts(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Preprocess trip contexts from Yelp data."""
    contexts = []
    businesses = data.get('businesses', [])
    
    for business in businesses:
        context = {
            'name': business.get('name', ''),
            'address': business.get('location', {}).get('address1', ''),
            'rating': business.get('rating', 0),
            'category': business.get('categories', []),
            'review_count': business.get('review_count', 0),
            'phone': business.get('phone', 'N/A'),
            'url': business.get('url', '')
        }
        contexts.append(context)
    
    return contexts

def encode_and_store_trip_contexts(contexts: List[Dict[str, Any]], namespace: str) -> None:
    """Encode and store trip contexts using new embedding generator."""
    for i, context in enumerate(contexts):
        text = f"{context['name']} is a {context['category']} located at {context['address']} with a rating of {context['rating']} based on {context['review_count']} reviews. Phone: {context['phone']}. Link: {context['url']}."
        
        # Use new embedding generator
        embedding = embedding_generator.generate_embedding(text)
        vectorIndex.update(f"{namespace}_{i}", embedding, context, namespace)

def fetch_weather_data(location: str, dates: List[str]) -> List[str]:
    """Fetch weather data using the new Weather client."""
    try:
        if not weather_client:
            print("Weather client not initialized")
            return []
        
        weather_info = []
        for date in dates:
            # Get weather forecast for the specific date
            forecast = weather_client.get_forecast(location, days=1)
            if forecast and forecast.get('forecast_days'):
                day_forecast = forecast['forecast_days'][0]
                weather_info.append(
                    f"Weather on {date}: {day_forecast['condition']}, "
                    f"high of {day_forecast['max_temp_c']}°C, "
                    f"low of {day_forecast['min_temp_c']}°C."
                )
        
        return weather_info
        
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return []

def fetch_flight_data(destination: str, dates: List[str]) -> List[str]:
    """Fetch flight data using the new Skyscanner client."""
    try:
        if not skyscanner_client:
            print("Skyscanner client not initialized")
            return []
        
        if len(dates) < 2:
            print("Need at least 2 dates for flight search")
            return []
        
        flight_info = []
        quotes_response = skyscanner_client.browse_quotes(
            origin='SFO',
            destination=destination,
            outbound_date=dates[0],
            inbound_date=dates[1]
        )
        
        if quotes_response and 'Quotes' in quotes_response:
            for quote in quotes_response['Quotes']:
                price = quote.get('MinPrice', 0)
                link = f"https://www.skyscanner.com/transport/flights/SFO/{destination}/{dates[0]}/{dates[1]}/"
                flight_info.append(f"Flight price: ${price}. [Book here]({link})")
        
        return flight_info
        
    except Exception as e:
        print(f"Error fetching flight data: {e}")
        return []

def extract_location_and_dates(query: str) -> Tuple[str, List[str]]:
    """Extract location and dates from query using spaCy."""
    doc = nlp(query)
    location = None
    dates = []

    for ent in doc.ents:
        if ent.label_ == "GPE":
            location = ent.text
        elif ent.label_ == "DATE":
            try:
                parsed_date = parse_date(ent.text, fuzzy=True)
                dates.append(parsed_date.strftime('%Y-%m-%d'))
            except ValueError:
                continue

    if not location:
        location = 'Bahamas'  # Default placeholder
    if len(dates) < 2:
        dates = ['2024-06-01', '2024-06-15']  # Default placeholders

    return location, dates
