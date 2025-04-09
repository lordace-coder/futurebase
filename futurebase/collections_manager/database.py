from pymongo import MongoClient
from pymongo.collection import Collection
# Connect to MongoDB (local instance)
client = MongoClient('mongodb://localhost:27017/')


# Select a database
db = client.collections_manager


def getCollection(collectionName:str)->Collection:
    return db.get_collection(collectionName)
