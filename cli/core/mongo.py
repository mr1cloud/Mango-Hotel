from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.database import Database

class MongoDB:
    def __init__(self, uri):
        self.uri = uri
        self.client = None

    def connect(self):
        try:
            self.client = MongoClient(self.uri)
            self.client.admin.command('ping')
            print("Connected to MongoDB successfully.")
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
            raise

    def get_database(self, db_name) -> Database:
        if self.client is None:
            raise ConnectionFailure("Not connected to MongoDB.")
        return self.client.get_database(db_name)

    def close(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")