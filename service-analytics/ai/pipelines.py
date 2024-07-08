from config.logger import log
from config.bootstrap import vectorIndex

from ai.pipelines.trip import initialize_trip_index, fetch_weather_data, fetch_flight_data, extract_location_and_dates
from ai.pipelines.pdf import initialize_pdf_index
from ai.pipelines.financial import initialize_financial_index

from ai.utils import generate_response


def direct_model_pipeline(query):
     return generate_response(query)

def pdf_rag_pipeline(query, query_embedding):
    initialize_pdf_index()
    search_results = vectorIndex.query(query_embedding, 5, 'pdfs')
    retrieved_contexts = [result['metadata'] for result in search_results['matches']]
    augmented_input = f"{query} {' '.join(retrieved_contexts)}"
    return generate_response(augmented_input)

def trip_rag_pipeline(query, query_embedding):
    location, dates = extract_location_and_dates(query)
    initialize_trip_index(location)
    
    weather_info = fetch_weather_data(location, dates)
    flight_info = fetch_flight_data(location, dates)
    
    search_results = vectorIndex.query(query_embedding, 5, 'trips')
    retrieved_contexts = [result['metadata'] for result in search_results['matches']]

    augmented_input = f"{query} {' '.join(retrieved_contexts + weather_info + flight_info)}"
    return generate_response(augmented_input)

def financial_rag_pipeline(query, query_embedding):
    initialize_financial_index()
    
    search_results = vectorIndex.query(query_embedding, 5, 'finance')
    retrieved_contexts = [result['metadata'] for result in search_results['matches']]

    augmented_input = f"{query} {' '.join(retrieved_contexts)}"
    return generate_response(augmented_input)
