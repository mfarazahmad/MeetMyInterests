
import sys
import asyncio
from traceback import format_exc

from config.logger import Logger, setLogger
from config.settings import Config

#  Connnect to Service & Instantiate Application
cfg = Config()
log = Logger(cfg.loglevel)
setLogger(log)
log.info("Retrieving Configuration")

from broker.nats import Broker
from database.pgx import Database
from database.pinecone import VectorDatabase
from vendors.aws.s3 import S3Client
from vendors.plaid.client import PlaidClient
from vendors.yelp.client import YelpClient
from vendors.weather.client import WeatherClient
from vendors.skyscanner.client import SkyscannerClient
from vendors.google.drive import GoogleDriveClient
from vendors.google.maps import GoogleMapsClient

# Connect To Broker
broker = None
broker_connected = False

async def initialize_broker():
    """Initialize NATS broker connection."""
    global broker, broker_connected
    
    try:
        broker = Broker(cfg.BrokerHost, cfg.BrokerTopic, cfg.BrokerGroup, cfg.BrokerTimeout)
        broker_connected = await broker.connect()
        
        if broker_connected:
            log.info("NATS Broker Initialization Successful")
        else:
            log.error("NATS Broker Initialization Failed")
            sys.exit(1)
            
    except Exception as e:
        log.error(f"NATS Broker Initialization Error: {e}")
        log.debug(f"{format_exc()}")
        sys.exit(1)

# Initialize broker synchronously for backward compatibility
def init_broker_sync():
    """Synchronous broker initialization for backward compatibility."""
    global broker, broker_connected
    
    try:
        broker = Broker(cfg.BrokerHost, cfg.BrokerTopic, cfg.BrokerGroup, cfg.BrokerTimeout)
        # For sync compatibility, we'll connect when needed
        log.info("NATS Broker created (will connect when needed)")
        broker_connected = False
    except Exception as e:
        log.error(f"NATS Broker Creation Error: {e}")
        sys.exit(1)

# Connect To Database
database = None
try:
    database = Database(cfg.dbHost, cfg.dbUser, cfg.dbPass, cfg.dbName, cfg.dbPort)
except Exception as e:
    log.error(f"Database Initialization Error: {e}")
    #log.debug(f"{format_exc()}")
    sys.exit(1)


# Connect To Vector Database (Pinecone)
vectorIndex = None
try:
    vectorIndex = VectorDatabase(cfg.vectorKey, cfg.vectorEnv, cfg.vectorIndex)
except Exception as e:
    log.error(f"Vector Database Initialization Error: {e}")
    #log.debug(f"{format_exc()}")
    sys.exit(1)

# Connect To S3
s3 = None
try:
    s3 = S3Client(cfg.awsID, cfg.awsRegion)
except Exception as e:
    log.error(f"S3 Initialization Error: {e}")
    #log.debug(f"{format_exc()}")
    sys.exit(1)

# Initialize Vendor Clients
plaid_client = None
try:
    plaid_client = PlaidClient()
except Exception as e:
    log.error(f"Plaid Client Initialization Error: {e}")

yelp_client = None
try:
    yelp_client = YelpClient()
except Exception as e:
    log.error(f"Yelp Client Initialization Error: {e}")

weather_client = None
try:
    weather_client = WeatherClient()
except Exception as e:
    log.error(f"Weather Client Initialization Error: {e}")

skyscanner_client = None
try:
    skyscanner_client = SkyscannerClient()
except Exception as e:
    log.error(f"Skyscanner Client Initialization Error: {e}")

google_drive_client = None
try:
    google_drive_client = GoogleDriveClient()
except Exception as e:
    log.error(f"Google Drive Client Initialization Error: {e}")

google_maps_client = None
try:
    google_maps_client = GoogleMapsClient()
except Exception as e:
    log.error(f"Google Maps Client Initialization Error: {e}")

# Initialize broker for backward compatibility
init_broker_sync()