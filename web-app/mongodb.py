from pymongo import MongoClient
from bson.json_util import dumps, loads
import certifi

class Database(object):

    url = "mongodb+srv://admin:admin123@cluster0.b6toxnx.mongodb.net/?retryWrites=true&w=majority"
    database=None
    client=None
    ca = certifi.where()
    
    @staticmethod
    def initialize():
        connection= MongoClient(Database.url, tlsCAFile=Database.ca)
        try:
            connection.admin.command('ping')
            Database.client=connection
            Database.database = connection["project_4"]
            print(' *', 'Connected to MongoDB!') 
        except Exception as e:
            print(' *', "Failed to connect to MongoDB at")
            print('Database connection error:', e)

    @staticmethod
    def insert_one(collection, data):
        return Database.database[collection].insert_one(data)

    @staticmethod
    def find(collection, query="", field=""):
        return (Database.database[collection].find(query,field))

    @staticmethod
    def find_single(collection, query, field=""):
        return (Database.database[collection].find_one(query,field))

    @staticmethod
    def delete(collection, query):
        return Database.database[collection].delete_one(query)

    @staticmethod
    def update(collection, search, query):
        return Database.database[collection].update_one(search,query)

    @staticmethod
    def count(collection, query):
        return Database.database[collection].count_documents(query)

    @staticmethod
    def close():
        Database.client.close()

