import os
import dotenv
from pymongo import MongoClient

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

CONNECTION_STRING = os.environ.get("MONGODB_STRING_CONNECTION")

connection = MongoClient(CONNECTION_STRING)