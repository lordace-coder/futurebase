from typing import Iterable
from bson import ObjectId  # Import ObjectId for handling MongoDB _id fields
import collections_manager.database as mongoclient


def fetchAllData(collectionId:str):
    return mongoclient.getCollection(collectionId).find()


def insertData(collectionId:str, data:dict|Iterable):
    if isinstance(data, dict):
        result = mongoclient.getCollection(collectionId).insert_one(data)
        return mongoclient.getCollection(collectionId).find_one({"_id": result.inserted_id})
    elif isinstance(data, Iterable):
        result = mongoclient.getCollection(collectionId).insert_many(data)
        return list(mongoclient.getCollection(collectionId).find({"_id": {"$in": result.inserted_ids}}))
    else:
        raise ValueError("Invalid data type")

def deleteData(collectionId:str,data,many=False, ):
    print(data)
    if not many:
        mongoclient.getCollection(collectionId).delete_one(data)
    else:
        mongoclient.getCollection(collectionId).delete_many(data)



def updateData(collectionId:str, *args, **kwargs):
    # Convert _id in the filter to ObjectId if it exists
    if 'filter' in kwargs and '_id' in kwargs['filter']:
        kwargs['filter']['_id'] = ObjectId(kwargs['filter']['_id'])

    result = mongoclient.getCollection(collectionId).update_one(*args, **kwargs)
    print(mongoclient.getCollection(collectionId).find().to_list())  # Debugging: Print all documents
    if result.matched_count == 0:
        raise ValueError("No matching document found to update.")
    return mongoclient.getCollection(collectionId).find_one({"_id": kwargs.get("filter", {}).get("_id")})
