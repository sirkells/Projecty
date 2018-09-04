from pymongo import MongoClient
import datetime
import re


def connect():
    connection = MongoClient('172.16.11.200', 27017)
    handle = connection["projectfinder"]
    return handle
db = connect()
#data = db.itproject.find({"region": None }) #None gets all doc without region field

#unset field
#unset region
db.itproject.update({"region":{"$exists": True }}, {"$unset":{"region": ""}}, multi=True)
#unset stack
db.itproject.update({"stack":{"$exists": True }}, {"$unset":{"stack": ""}}, multi=True)