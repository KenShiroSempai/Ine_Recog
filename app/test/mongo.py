from pymongo import MongoClient

# MongoDB connection string
connection_string = "mongodb://root:example@192.168.100.8:2017/"

# Create a MongoClient to the running mongod instance
client = MongoClient(connection_string)

# You can access the Database using dictionary-style access:
db = client['your_database_name']
