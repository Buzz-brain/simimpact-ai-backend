# app/database.py
import motor.motor_asyncio
from bson import ObjectId

MONGO_URL = "mongodb+srv://chinomsochristian03:ejw3sYW64rOxh44g@cluster0.lvarax1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.simimpact

# Helper to convert ObjectId to string
def to_dict(obj):
    obj["_id"] = str(obj["_id"])
    return obj
