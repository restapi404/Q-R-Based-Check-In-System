'''from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
import os
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# MongoDB configuration
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

def get_database():
    """Returns a connected database instance with error handling"""
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
        
        # Verify connection
        client.admin.command('ping')
        print("> Successfully connected to MongoDB")  # Removed Unicode symbol
        
        return client["qr_event_checkin"]
        
    except ConnectionFailure as e:
        print(f"> MongoDB connection failed: {e}")
        sys.exit(1)
    except PyMongoError as e:
        print(f"> MongoDB error: {e}")
        sys.exit(1)

# Initialize database connection
db = get_database()'''

'''from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
db = client["event_checkin"]

# Create default events if none exist
if db.events.count_documents({}) == 0:
    db.events.insert_many([
        {
            "title": "Techno Hackathon",
            "date": "2024-05-03",
            "description": "24-hour coding competition",
            "location": "CS Lab"
        },
        {
            "title": "Ammuno Workshop", 
            "date": "2024-05-08",
            "description": "Hands-on robotics session",
            "location": "Engineering Block"
        }
    ])'''

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
db = client["event_checkin"]

# Create default events if none exist
if db.events.count_documents({}) == 0:
    db.events.insert_many([
        {
            "id": "1",
            "title": "Techno Hackathon",
            "date": "2024-05-03",
            "description": "24-hour coding competition",
            "location": "CS Lab"
        },
        {
            "id": "2",
            "title": "Ammuno Workshop", 
            "date": "2024-05-08",
            "description": "Hands-on robotics session",
            "location": "Engineering Block"
        }
    ])
