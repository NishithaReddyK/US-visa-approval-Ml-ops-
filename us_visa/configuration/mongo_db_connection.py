import sys
import os
import pymongo
import certifi

from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.constants import DATABASE_NAME, MONGODB_URL_KEY

ca = certifi.where()

class MongoDBClient:
    """
    Class Name :   MongoDBClient
    Description :   This class initializes a connection to the MongoDB database.

    Output      :   Connection to MongoDB database
    On Failure  :   Raises USvisaException
    """
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)

                # Debug print
                print(f"Raw mongo URL from env: {mongo_db_url!r}")

                # Strip extra surrounding quotes if any
                if mongo_db_url:
                    mongo_db_url = mongo_db_url.strip().strip('"').strip("'")

                if mongo_db_url is None or not mongo_db_url.startswith(("mongodb://", "mongodb+srv://")):
                    raise Exception(f"Invalid MongoDB URL or environment key '{MONGODB_URL_KEY}' is not set properly.")

                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB connection successful")

        except Exception as e:
            raise USvisaException(e, sys)
