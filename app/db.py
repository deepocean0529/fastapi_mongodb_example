import os

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError

from app.resources.logger import logger


class MongoManager:
    client: MongoClient = None
    db: Database = None

    def get_connection_info(self):
        ENVIRONMENT = os.environ.get("ENVIRONMENT")

        MONGODB_URL: str
        MONGODB_DBNAME: str

        if ENVIRONMENT == "local":
            MONGODB_URL = os.environ.get("MONGODB_URL_LOCAL")
            MONGODB_DBNAME = os.environ.get("MONGODB_DBNAME_LOCAL")

        return {"url": MONGODB_URL, "dbname": MONGODB_DBNAME}

    def connect_to_database(self):
        info = self.get_connection_info()

        logger.info("Connecting to MongoDB.")

        try:
            self.client = MongoClient(info["url"], serverSelectionTimeoutMS=3000)
            self.client.is_mongos
            self.db = self.client[info["dbname"]]
            logger.info("Connected to MongoDB.")
        except:
            logger.error("Failed to connect to MongoDB.")

    def close_database_connection(self):
        logger.info("Closing connection with MongoDB.")

        self.client.close()

        logger.info("Closed connection with MongoDB.")


dbm = MongoManager()
