from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timezone

# Connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017")

# Select the database and collection
db = client["CSIR"]
collection = db["vpn"]

# Find all documents in the collection
documents = collection.find()

# Create a new collection for storing the creation times
creation_times_collection = db["creation_times"]

# Iterate through the documents
for document in documents:
    # Get the ObjectId of the document
    oid = ObjectId(document["_id"])

    # Convert the ObjectId to a datetime object
    creation_time = datetime.fromtimestamp(oid.generation_time, tz=timezone.utc)

    # Create a new document for the creation time
    creation_time_document = {"_id": oid, "creation_time": creation_time}

    # Insert the document into the new collection
    creation_times_collection.insert_one(creation_time_document)

# Iterate through the documents in the new collection
for creation_time_document in creation_times_collection.find():
    # Print the creation time
    print(creation_time_document["creation_time"])