# app/database.py

import os
import motor.motor_asyncio
from bson import ObjectId

MONGO_URI = os.getenv("MONGO_URI")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.simimpact

# Helper to convert ObjectId to string
def to_dict(obj):
    obj["_id"] = str(obj["_id"])
    return obj
