import os
import requests
import spacy
from dateutil.parser import parse as parse_date

from ai.utils import tokenizer, context_encoder
from config.bootstrap import vectorIndex

nlp = spacy.load("en_core_web_sm")

def initialize_trip_index(location):
    types = ['restaurants', 'activities', 'hotels', 'hospitals']
    for term in types:
        data = fetch_yelp_data(location, term)
        contexts = preprocess_trip_contexts(data)
        encode_and_store_trip_contexts(contexts, namespace='trips')

def fetch_yelp_data(location, term):
    YELP_API_KEY = os.getenv('YELP_API_KEY')
    headers = {'Authorization': f'Bearer {YELP_API_KEY}'}
    url = 'https://api.yelp.com/v3/businesses/search'
    params = {'location': location, 'term': term, 'limit': 5}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def preprocess_trip_contexts(data):
    contexts = []
    for business in data['businesses']:
        context = {
            'name': business['name'],
            'address': " ".join(business['location']['display_address']),
            'rating': business['rating'],
            'category': ", ".join([cat['title'] for cat in business['categories']]),
            'review_count': business['review_count'],
            'phone': business.get('phone', 'N/A'),
            'url': business.get('url', '')
        }
        contexts.append(context)
    return contexts

def encode_and_store_trip_contexts(contexts, namespace):
    for i, context in enumerate(contexts):
        text = f"{context['name']} is a {context['category']} located at {context['address']} with a rating of {context['rating']} based on {context['review_count']} reviews. Phone: {context['phone']}. Link: {context['url']}."
        inputs = tokenizer(text, return_tensors='tf', truncation=True)
        embedding = context_encoder(**inputs).pooler_output.numpy().squeeze()
        vectorIndex.update(f"{namespace}_{i}", embedding, context, namespace)

def fetch_weather_data(location, dates):
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
    url = 'http://api.weatherapi.com/v1/forecast.json'
    params = {'key': WEATHER_API_KEY, 'q': location, 'days': len(dates)}
    response = requests.get(url, params=params)
    forecast_data = response.json()
    
    weather_info = []
    for i, date in enumerate(dates):
        day_forecast = forecast_data['forecast']['forecastday'][i]
        weather_info.append(
            f"Weather on {date}: {day_forecast['day']['condition']['text']}, "
            f"high of {day_forecast['day']['maxtemp_c']}°C, "
            f"low of {day_forecast['day']['mintemp_c']}°C."
        )
    
    return weather_info

def fetch_flight_data(destination, dates):
    SKYSCANNER_API_KEY = os.getenv('SKYSCANNER_API_KEY')
    url = 'https://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/US/USD/en-US'
    params = {
        'apiKey': SKYSCANNER_API_KEY,
        'originplace': 'SFO-sky',
        'destinationplace': f'{destination}-sky',
        'outbounddate': dates[0],
        'inbounddate': dates[1],
    }
    response = requests.get(url, params=params)
    flight_data = response.json()

    flight_info = []
    for quote in flight_data.get('Quotes', []):
        price = quote['MinPrice']
        link = f"https://www.skyscanner.com/transport/flights/SFO/{destination}/{dates[0]}/{dates[1]}/"
        flight_info.append(f"Flight price: ${price}. [Book here]({link})")
    
    return flight_info

def extract_location_and_dates(query):
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
