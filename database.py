from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
db = client["event_checkin"]

# Clear and reinitialize collections
db.users.drop()
db.events.drop()
db.registrations.drop()

# Insert test events
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
print("Database initialized with test data")