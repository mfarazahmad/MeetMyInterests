from config.logger import log
from config.bootstrap import vectorIndex

from ai.pipelines.trip import initialize_trip_index, fetch_weather_data, fetch_flight_data, extract_location_and_dates
from ai.pipelines.pdf import initialize_pdf_index
from ai.pipelines.financial import initialize_financial_index

from ai.rag_pipeline import rag_pipeline
from ai.prompt_engineer import TaskType


def direct_model_pipeline(query):
    """Direct model pipeline without RAG."""
    from ai.utils import response_generator
    return response_generator.generate_response(query)


def pdf_rag_pipeline(query, query_embedding):
    """PDF RAG pipeline with hybrid search and structured prompting."""
    try:
        # Initialize PDF index
        initialize_pdf_index()
        
        # Process query using RAG pipeline
        response = rag_pipeline.process_pdf_query(query)
        
        return response
    except Exception as e:
        log.error(f"Error in PDF RAG pipeline: {e}")
        return f"I apologize, but I encountered an error while processing your PDF query: {str(e)}"


def trip_rag_pipeline(query, query_embedding):
    """Trip RAG pipeline with hybrid search and structured prompting."""
    try:
        # Extract location and dates
        location, dates = extract_location_and_dates(query)
        
        # Initialize trip index
        initialize_trip_index(location)
        
        # Fetch additional context
        weather_info = fetch_weather_data(location, dates)
        flight_info = fetch_flight_data(location, dates)
        
        # Combine additional context
        additional_context = weather_info + flight_info
        
        # Process query using RAG pipeline
        response = rag_pipeline.process_trip_query(query, additional_context)
        
        return response
    except Exception as e:
        log.error(f"Error in trip RAG pipeline: {e}")
        return f"I apologize, but I encountered an error while processing your trip query: {str(e)}"


def financial_rag_pipeline(query, query_embedding):
    """Financial RAG pipeline with hybrid search and structured prompting."""
    try:
        # Initialize financial index
        initialize_financial_index()
        
        # Process query using RAG pipeline
        response = rag_pipeline.process_financial_query(query)
        
        return response
    except Exception as e:
        log.error(f"Error in financial RAG pipeline: {e}")
        return f"I apologize, but I encountered an error while processing your financial query: {str(e)}"


def health_rag_pipeline(query, query_embedding):
    """Health advice RAG pipeline with hybrid search and structured prompting."""
    try:
        # Process query using RAG pipeline
        response = rag_pipeline.process_health_query(query)
        
        return response
    except Exception as e:
        log.error(f"Error in health RAG pipeline: {e}")
        return f"I apologize, but I encountered an error while processing your health query: {str(e)}"


def productivity_rag_pipeline(query, query_embedding):
    """Productivity RAG pipeline with hybrid search and structured prompting."""
    try:
        # Process query using RAG pipeline
        response = rag_pipeline.process_productivity_query(query)
        
        return response
    except Exception as e:
        log.error(f"Error in productivity RAG pipeline: {e}")
        return f"I apologize, but I encountered an error while processing your productivity query: {str(e)}"
