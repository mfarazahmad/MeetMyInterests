
# TODO: Create Tables
# TODO: Connect to Google Drive, Sheets, Docs
# TODO: Migrate Google Data to Pandas
# TODO: Change PDF to Pandas

# TODO: Cron to Train Model Weekly
# TODO: Cron to remove old Model
# TODO; Implement Circuit Breaker
# TODO: Implement Retry Logic

from flask import Flask
from flask_socketio import SocketIO, emit

from apscheduler.schedulers.background import BackgroundScheduler

from ai.pipelines import direct_model_pipeline, pdf_rag_pipeline, trip_rag_pipeline, financial_rag_pipeline
from ai.training import train_trip_model, train_financial_data, train_pdf_data
from ai.utils import encode_query

from config.bootstrap import broker
from config.logger import log

# Websocket for Queries
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('message')
def handle_message(data):
    query = data['query']
    query_embedding = encode_query(query)

    if "book" in query.lower():
        response = pdf_rag_pipeline(query, query_embedding)
    elif "finance" in query.lower():
        response = financial_rag_pipeline(query, query_embedding)
    elif "trip" in query.lower():
        response = trip_rag_pipeline(query, query_embedding)
    else:
        response = direct_model_pipeline(query)

    emit('response', {'answer': response})

# Scheduler for Training
def schedule_training():
    scheduler = BackgroundScheduler()
    scheduler.add_job(train_trip_model, 'interval', weeks=1, kwargs={'new_only': False})
    scheduler.add_job(train_trip_model, 'interval', days=1, kwargs={'new_only': True})
    scheduler.add_job(train_financial_data, 'interval', weeks=1, kwargs={})
    scheduler.add_job(train_pdf_data, 'interval', weeks=1, kwargs={})
    scheduler.start()

def setup():
    log.info("Configuration Complete")
    broker.listen()


if __name__ == "__main__":
    setup()
    schedule_training()
    socketio.run(app)