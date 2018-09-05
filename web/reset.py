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
db.itproject.update({"region1":{"$exists": True }}, {"$unset":{"region1": ""}}, multi=True)
#unset stack
db.itproject.update({"stack":{"$exists": True }}, {"$unset":{"stack": ""}}, multi=True)
db.itproject.update({"fullstack_type":{"$exists": True }}, {"$unset":{"fullstack_type": ""}}, multi=True)


#db.itproject.update({"skill_summary": {"$regex": 'node'}}, {"skill_summary": {"$regex": '(js|javascript|react|angular|vue|css|express|html|bootstrap)'}]}, "title":{"$regex": '(Node|Fullstack Javascript)', "$options": 'i'}}, {"$set":{"stack": "Fullstack"}}, multi=True)
#db.itproject.update({"skill_summary": {"$all": [ 'javascript', 'node.js']},"title":{"$regex": '(Node|Fullstack Javascipt)', "$options": 'i'}}, {"$set":{"stack": "Node Fullstack"}}, multi=True)
#db.itproject.update({"skill_summary": {"$all": [{"$regex": 'node'}, {"$regex": '(^js|javascript|react|angular|vue|css|express|html|bootstrap)'}]},"title":{"$regex": '(Node|Fullstack Javascipt)', "$options": 'i'}}, {"$set":{"stack": "Node Fullstack"}}, multi=True)
#db.itproject.update({"skill_summary": {"$all": [{"$regex": 'node'}, {"$regex": '(^js|javascript|react|angular|vue|css|express|html|bootstrap)'}]}}, {"$set":{"stack": "Node Fullstack"}}, multi=True)

#{$and: [ { skill_summary: RegExp(/node/i) }, { skill_summary: RegExp(/^js/) } ]}
#{skill_summary: {$all: [RegExp(/node/), RegExp(/^js/)]}}

#db.itproject.update({"skill_summary": {"$all": ['node.js', 'js']},"title":{"$regex": '(Node|Fullstack Javascript)', "$options": 'i'}}, {"$set":{"stack": "Fullstack"}}, multi=True)

#db.itproject.update({"skill_summary": {"$all": ['nodejs', 'js']}}, {"$set":{"stack": "Fullstack"}}, multi=True)

#skills with title
db.itproject.update({ "$and": [ { "skill_summary": {"$regex": '(python|django|flask|pyramid)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ], "title":{"$regex": '(Python|Fullstack Python|Python Fullstack)', "$options": 'i'}}, {"$set":{"stack": ["Fullstack", "Python"]}}, multi=True)
db.itproject.update({ "$and": [ { "skill_summary": {"$regex": r'(?:[\s]|^)(java|spring|j2ee)(?=[\s]|$)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ], "title":{"$regex": '(Java|Fullstack Java|Java Fullstack)', "$options": 'i'}}, {"$set":{"stack": ["Fullstack", "Java"]}}, multi=True)
db.itproject.update({ "$and": [ { "skill_summary": {"$regex": '(php|laravel)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ], "title":{"$regex": '(php|Fullstack php|php Fullstack|laravel)', "$options": 'i'}}, {"$set":{"stack": ["Fullstack", "PHP"]}}, multi=True)
db.itproject.update({ "$and": [ { "skill_summary": {"$regex": '(node|express)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|express|html|bootstrap|jquery)'} } ], "title":{"$regex": '(php|Fullstack php|php Fullstack|laravel)', "$options": 'i'}}, {"$set":{"stack": ["Fullstack", "Node"]}}, multi=True)

#skills without title
db.itproject.update({ "$and": [ { "skill_summary": {"$regex": r'(?:[\s]|^)(java|spring|j2ee)(?=[\s]|$)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ] }, {"$set":{"stack": ["Fullstack", "Java"]}}, multi=True)
db.itproject.update({ "$and": [ { "skill_summary": {"$regex": '(python|django|flask|pyramid)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ] }, {"$set":{"stack": ["Fullstack", "Python"]}}, multi=True)
db.itproject.update({ "$and": [ { "skill_summary": {"$regex": '(php|laravel)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ]}, {"$set":{"stack": ["Fullstack", "PHP"]}}, multi=True)
db.itproject.update({ "$and": [ { "skill_summary": {"$regex": '(node|express)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery|express)'} } ]}, {"$set":{"stack": ["Fullstack", "Node"]}}, multi=True)


#db.itproject.update({ "$and": [ { "stack": 'Fullstack'}, { "skill_summary": {"$regex": '(php|laravel)'} } ]}, {"$set":{"fullstack_type": "PHP"}}, multi=True)
#db.itproject.update({ "$and": [ { "stack": 'Fullstack'}, { "skill_summary": {"$regex": r'(?:[\s]|^)(java|spring|j2ee)(?=[\s]|$)'} } ]}, {"$set":{"fullstack_type": "Java"}}, multi=True)
#db.itproject.update({ "$and": [ { "skill_summary": {"$regex": r'(?:[\s]|^)(java)(?=[\s]|$)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|express|html|bootstrap|jquery)'} } ], "title":{"$regex": '(Java|Fullstack Java|Java Fullstack)', "$options": 'i'}}, {"$set":{"stack": "Fullstack"}}, multi=True)
#db.itproject.update({ "$and": [ { "skill_summary": {"$regex": 'php'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|express|html|bootstrap|jquery)'} } ], "title":{"$regex": '(php|Fullstack php|php Fullstack|laravel)', "$options": 'i'}}, {"$set":{"stack": "Fullstack"}}, multi=True)