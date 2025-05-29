import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv() 

MONGO_DETAILS = os.environ.get("MONGO_DETAILS", "mongodb://admin:password@localhost:27017")

client: AsyncIOMotorClient = None
database = None

async def connect_to_mongo():
    global client
    global database
    print(f"Attempting to connect to MongoDB at: {MONGO_DETAILS}")
    client = AsyncIOMotorClient(MONGO_DETAILS)
    database = client.library_db_lab5 
    print("Successfully connected to MongoDB and selected database.")
    try:
        await database.list_collection_names()
        print("MongoDB connection verified.")
    except Exception as e:
        print(f"MongoDB connection/verification failed: {e}")


async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("MongoDB connection closed.")

def get_database():
    if database is None:
        raise Exception("Database not initialized. Call connect_to_mongo first.")
    return database