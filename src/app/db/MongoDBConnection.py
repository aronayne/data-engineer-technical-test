import pymongo

from src.app.config import AppConfig
from src.app.db.DBConnectionURIBuilder import DBConnectionURIBuilder


"""
Manage the connection to MongoDB.
Uses the context manager pattern
"""
class MongoDBConnection(object):

    def __init__(self):
        self.connection_string = DBConnectionURIBuilder.build(AppConfig.mongo_db_username, AppConfig.mongo_db_password)
        self.db = None
        self.client = None

    def __enter__(self):
        self.client = pymongo.MongoClient(self.connection_string)
        self.db = self.client.technicalTestDB
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
