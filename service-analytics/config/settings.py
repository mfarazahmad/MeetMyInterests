
import os
from dotenv import load_dotenv

cfg = None

class Config():
    def __init__(self):
        secrets = self.getSecrets()

        # Database Details
        self.dbUser = secrets['pgx']['user']
        self.dbPass = secrets['pgx']['password']
        self.dbHost = secrets['pgx']['host']
        self.dbName = secrets['pgx']['name']
        self.dbPort = secrets['pgx']['port']

        # Broker Details
        self.BrokerTopic = secrets['broker']['topic']
        self.BrokerGroup = secrets['broker']['group']
        self.BrokerHost = secrets['broker']['host']
        self.BrokerTimeout = secrets['broker']['timeout']

        # Model Location
        self.modelPath = secrets['model']['path']
        self.modelName = secrets['model']['name']

        # Vector Database Details
        self.vectorKey = secrets['vector']['key']
        self.vectorEnv = secrets['vector']['env']
        self.vectorIndex = secrets['vector']['index']

        # AWS ENV
        self.awsRegion = secrets['aws']['region']
        self.awsKey = secrets['aws']['key']
        self.awsID = secrets['aws']['id']

        self.loglevel = secrets['log']['level']

    def pullFromEnv(self, secretName, default=""):
        secret = os.environ.get(secretName, default)
        return secret

    def getSecrets(self):
        # Load in Config from env
        load_dotenv()
        secrets = {
            "pgx": {
                "host": self.pullFromEnv("DB_HOST"),
                "port": self.pullFromEnv("DB_PORT"),
                "user": self.pullFromEnv("DB_USERNAME"),
                "password": self.pullFromEnv("DB_PASS"),
                "name": self.pullFromEnv("DB_NAME"),
            },
            "broker" : {
                "topic": self.pullFromEnv("BROKER_TOPIC"),
                "group":  self.pullFromEnv("BROKER_GROUP"),
                "host": self.pullFromEnv("BROKER_HOST"),
                "timeout":  self.pullFromEnv("BROKER_TIMEOUT"),
            },
            "model": {
                "path": self.pullFromEnv("MODEL_PATH"),
                "name": self.pullFromEnv("MODEL_NAME"),
            },
            "vector": {
                "key": self.pullFromEnv("PINECONE_API_KEY"),
                "env":  self.pullFromEnv("PINECONE_ENVIRONMENT"),
                "index": self.pullFromEnv("PINECONE_INDEX"),
            },
            "aws": {
                "id": self.pullFromEnv('AWS_ACCESS_KEY_ID'),
                "key": self.pullFromEnv('AWS_SECRET_ACCESS_KEY'),
                "region": self.pullFromEnv('AWS_REGION')
            },
            "log": {
                "level": self.pullFromEnv("LOGLEVEL", "INFO"),
            }
        }
        return secrets
    
