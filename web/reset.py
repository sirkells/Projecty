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



#db.itproject.update({"skill_summary": {"$regex": 'node'}}, {"skill_summary": {"$regex": '(js|javascript|react|angular|vue|css|express|html|bootstrap)'}]}, "title":{"$regex": '(Node|Fullstack Javascript)', "$options": 'i'}}, {"$set":{"stack": "Fullstack"}}, multi=True)

db.itproject.update({"skill_summary": {"$all": [{"$regex": 'node'}, {"$regex": '(^js|javascript|react|angular|vue|css|express|html|bootstrap)'}]},"title":{"$regex": '(Node|Fullstack Javascipt)', "$options": 'i'}}, {"$set":{"stack": "Node Fullstack"}}, multi=True)
db.itproject.update({"skill_summary": {"$all": [{"$regex": 'node'}, {"$regex": '(^js|javascript|react|angular|vue|css|express|html|bootstrap)'}]}}, {"$set":{"stack": "Node Fullstack"}}, multi=True)

#{$and: [ { skill_summary: RegExp(/node/i) }, { skill_summary: RegExp(/^js/) } ]}
#{skill_summary: {$all: [RegExp(/node/), RegExp(/^js/)]}}