import sys
from loguru import logger

log = None

class Logger():

    def __init__(self, loglevel):
        logger.remove(0) # remove the default handler configuration
        logger.add(sys.stderr, level=loglevel)
        self.logger = logger

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warn(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

def setLogger(instance):
    global log 
    log = instance
    