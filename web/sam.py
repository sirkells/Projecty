from pymongo import MongoClient
import datetime
import re
import pymongo


def connect():
    connection = MongoClient('127.0.0.1', 27017)
    handle = connection["students"]
    return handle
db = connect()
data = db.grades.find({'type': 'homework'})
ab = data.sort([('student_id', pymongo.ASCENDING),
                     ('score', pymongo.DESCENDING)])
print(data.count())
print(ab)

"""print(data1.count())

for title in data1:
    if title['title'] && title['skills'] == 'None':
        pass
    print(title)
"""