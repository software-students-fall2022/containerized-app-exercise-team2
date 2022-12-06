from pymongo import MongoClient
import mongomock
from bson.json_util import dumps, loads
import certifi
import sys
from datetime import datetime, date

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
            print(' *', 'Connected to MongoDB!', file=sys.stderr)
        except Exception as e:
            print(' *', "Failed to connect to MongoDB at", file=sys.stderr)
            print('Database connection error: ' + e, file=sys.stderr)

    @staticmethod
    def initialize_mock():
        Database.database = mongomock.MongoClient().db

    @staticmethod
    def insert_one(collection, data):
        return Database.database[collection].insert_one(data)

    @staticmethod
    def find(collection, query="", field=""):
        return (Database.database[collection].find(query,field))

    @staticmethod
    def find_single(collection, query, field=""):
        #print(Database.database, file=sys.stderr);
        return (Database.database[collection].find_one(query,field))

    @staticmethod
    def find_first_sorted(collection, query, field=""):
        #print(Database.database, file=sys.stderr);
        return (Database.database[collection].find(query,field).sort('time', -1).limit(1))

    @staticmethod
    def delete(collection, query):
        return Database.database[collection].delete_one(query)

    @staticmethod
    def update(collection, search, query):
        return Database.database[collection].update_one(search,query)

    @staticmethod
    def findWeekly(collection, query="", field=""):
        return (Database.database[collection].aggregate([{
                '$match': query
            }, {
                '$group': {
                    '_id':{
                        "$let": {
                          "vars": {
                            "dayMillis": 1000 * 60 * 60 * 24,
                            "beginWeek": {
                              "$subtract": [
                                { "$subtract": [ "$time", datetime(1970, 1, 1) ] },
                                { "$cond": [
                                  { "$eq": [{ "$dayOfWeek": "$time" }, 1 ] },
                                  0,
                                  { "$multiply": [
                                    1000 * 60 * 60 * 24,
                                    { "$subtract": [{ "$dayOfWeek": "$time" }, 1 ] }
                                  ]}
                                ]}
                              ]
                            }
                          },
                          "in": {
                            "$subtract": [
                              "$$beginWeek",
                              { "$mod": [ "$$beginWeek", "$$dayMillis" ]}
                            ]
                          }
                        }
                      },
                      "Moo": { "$first": "$mood" },
                    "Date":{ "$first": "$time" },
                    "count": {"$sum": 1}
                }
            }, {
                '$sort': {"Moo": 1, "count": -1}
            }, {
                '$group': {
                    "_id": "$_id",
                    "mood": {"$first": "$Moo"},
                    "date": {"$first": "$Date"}
                }
            }
        ]))

    @staticmethod
    def close():
        Database.client.close()
