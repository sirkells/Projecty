from pymongo import MongoClient
import datetime
import re
import pymongo


def connect():
    connection = MongoClient('127.0.0.1', 27017)
    handle = connection["students"]
    return handle
db = connect()
ha = db.grades.find()
data = db.grades.find({'type': 'homework'})
ab = data.sort([('student_id', pymongo.ASCENDING),
                     ('score', pymongo.ASCENDING)])
print(data)
print(data[0])
print(data[1])
print(data[2])
print(data.count())
print
ans = []


for a in ab:
  

    ans.append(a)

del ans[0::2]
print(len(ans))


for city in ans:
    big = city['score']
    db.grades.update({"type":'homework'}, {"$set":{"score": big}}, multi=True)
s = db.grades.find()
print(db.grades.find().count())
print(s[0])
print(s[1])
print(s[2])
db.grades.aggregate( { '$group' : { '_id' : '$student_id', 'average' : { '$avg' : '$score' } } }, { '$sort' : { 'average' : -1 } }, { '$limit' : 1 } )




"""print(data1.count())

for title in data1:
    if title['title'] && title['skills'] == 'None':
        pass
    print(title)
"""