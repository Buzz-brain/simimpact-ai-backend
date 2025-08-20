# app/database.py

import os
import motor.motor_asyncio
from bson import ObjectId

MONGO_URL = os.getenv("MONGO_URL")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.simimpact

# Helper to convert ObjectId to string
def to_dict(obj):
    obj["_id"] = str(obj["_id"])
    return obj
