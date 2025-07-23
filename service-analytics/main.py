
# TODO: Create Tables
# TODO: Connect to Google Drive, Sheets, Docs
# TODO: Migrate Google Data to Pandas
# TODO: Change PDF to Pandas

# TODO: Cron to Train Model Weekly
# TODO: Cron to remove old Model
# TODO; Implement Circuit Breaker
# TODO: Implement Retry Logic

import asyncio
import threading
from flask import Flask
from flask_socketio import SocketIO, emit

from apscheduler.schedulers.background import BackgroundScheduler

import ai.pipelines as pipelines
from ai.training import train_trip_model, train_financial_data, train_pdf_data
from ai.utils import encode_query

from config.bootstrap import broker, initialize_broker
from config.logger import log

# Websocket for Queries
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('message')
def handle_message(data):
    query = data['query']
    query_embedding = encode_query(query)

    if "book" in query.lower():
        response = pipelines.pdf_rag_pipeline(query, query_embedding)
    elif "finance" in query.lower():
        response = pipelines.financial_rag_pipeline(query, query_embedding)
    elif "trip" in query.lower():
        response = pipelines.trip_rag_pipeline(query, query_embedding)
    else:
        response = pipelines.direct_model_pipeline(query)

    emit('response', {'answer': response})

# Message handler for NATS
async def nats_message_handler(data):
    """Handle messages from NATS broker."""
    try:
        message_type = data.get('type', 'unknown')
        action = data.get('action', '')
        message_data = data.get('data', {})
        
        log.info(f"Processing NATS message: {message_type} - {action}")
        
        if message_type == 'financial':
            if action == 'analyze_transactions':
                # Trigger financial analysis
                user_id = message_data.get('user_id')
                date_range = message_data.get('date_range')
                log.info(f"Analyzing transactions for user {user_id}, range: {date_range}")
                # Add your financial processing logic here
                
        elif message_type == 'pdf':
            if action == 'process_document':
                # Trigger PDF processing
                file_id = message_data.get('file_id')
                folder_id = message_data.get('folder_id')
                log.info(f"Processing PDF document: {file_id} from folder: {folder_id}")
                # Add your PDF processing logic here
                
        elif message_type == 'trip':
            if action == 'plan_trip':
                # Trigger trip planning
                destination = message_data.get('destination')
                dates = message_data.get('dates', [])
                log.info(f"Planning trip to {destination} on dates: {dates}")
                # Add your trip planning logic here
                
        else:
            log.warning(f"Unknown message type: {message_type}")
            
    except Exception as e:
        log.error(f"Error processing NATS message: {e}")

# Scheduler for Training
def schedule_training():
    """Initialize and start the training scheduler."""
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(train_trip_model, 'interval', weeks=1, kwargs={'new_only': False})
        scheduler.add_job(train_trip_model, 'interval', days=1, kwargs={'new_only': True})
        scheduler.add_job(train_financial_data, 'interval', weeks=1, kwargs={})
        scheduler.add_job(train_pdf_data, 'interval', weeks=1, kwargs={})
        scheduler.start()
        log.info("Training scheduler started successfully")
    except Exception as e:
        log.error(f"Failed to start training scheduler: {e}")

async def setup_async():
    """Async setup function for NATS broker."""
    log.info("Starting async configuration...")
    
    try:
        # Initialize NATS broker
        await initialize_broker()
        
        if broker:
            # Subscribe to messages
            await broker.subscribe(nats_message_handler)
            log.info("NATS broker subscribed and ready")
        else:
            log.error("Failed to initialize NATS broker")
    except Exception as e:
        log.error(f"Error in async setup: {e}")

def setup():
    """Synchronous setup function for backward compatibility."""
    log.info("Configuration Complete")
    
    # Start NATS in a separate thread to avoid blocking Flask
    def run_nats_setup():
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(setup_async())
            # Keep the loop running for NATS
            loop.run_forever()
        except Exception as e:
            log.error(f"Error in NATS setup thread: {e}")
        finally:
            try:
                loop.close()
            except:
                pass
    
    # Start NATS in background thread
    nats_thread = threading.Thread(target=run_nats_setup, daemon=True)
    nats_thread.start()
    
    log.info("NATS broker setup initiated in background thread")

if __name__ == "__main__":
    setup()
    schedule_training()
    socketio.run(app, debug=False, host='0.0.0.0', port=5000)