
import sys
from traceback import format_exc

from config.logger import Logger, setLogger
from config.settings import Config

#  Connnect to Service & Instantiate Application
cfg = Config()
log = Logger(cfg.loglevel)
setLogger(log)
log.info("Retrieving Configuration")

from broker.kakfa import Broker
from database.pgx import Database
from database.pinecone import VectorDatabase
from vendors.aws.s3 import Bucket

# Connect To Broker
broker = None
try:
    broker = Broker(cfg.BrokerHost, cfg.BrokerTopic, cfg.BrokerGroup, cfg.BrokerTimeout)
except Exception as e:
    log.error(f"Broker Initialization Error: {e}")
    #log.debug(f"{format_exc()}")
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

# Connect To Bucket
s3 = None
try:
    s3 = Bucket(cfg.awsID, cfg.awsKey, cfg.awsRegion)
except Exception as e:
    log.error(f"Bucket Initialization Error: {e}")
    #log.debug(f"{format_exc()}")
    sys.exit(1)