import os
import urllib.parse
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables from a .env file if needed
load_dotenv()

# MongoDB connection string (use environment variable for security)
# MONGODB_URL = os.environ.get("MongoDB_connection_string") # mine say it error rfc sth. idk
username = urllib.parse.quote_plus(os.getenv("MONGODB_USERNAME"))
password = urllib.parse.quote_plus(os.getenv("MONGODB_PASSWORD"))
MONGODB_URL = 'mongodb+srv://%s:%s@trondb.dcxup.mongodb.net' % (username, password)

# Create a MongoDB client
client = AsyncIOMotorClient(MONGODB_URL)

# Access the specific database
db = client.get_database("tron")

# Collections
game_collection = db.get_collection("game")
bounty_collection = db.get_collection("bounty")
nft_collection = db.get_collection("nft")
user_collection = db.get_collection("user")
orderitem_collection = db.get_collection("orderitem")
order_collection = db.get_collection("order")
verifiedpurchase_collection = db.get_collection("verifiedpurchase")

