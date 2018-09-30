from pymongo import MongoClient
import datetime
import re
from bundeslander import Baden_Württemberg, Bayern, Berlin, Brandenburg, Bremen, Hamburg, Hessen, Mecklenburg_Vorpommern, Niedersachsen, Nordrhein_Westfalen, Rheinland_Pfalz, Saarland, Sachsen, Sachsen_Anhalt, Schleswig_Holstein, Thüringen, Ausland

def connect():
    connection = MongoClient('127.0.0.1', 27017)
    handle = connection["projectfinder"]
    return handle
db = connect()
#data = db.itproject.find({"region.bundesland": None }) #None gets all doc without region.bundesland field


#db.itproject.update({"region1":{"$exists": True }}, {"$unset":{"region1": ""}}, multi=True)
#unset bereich
db.itproject.update({"region":{"$exists": True }}, {"$unset":{"region": ""}}, multi=True)
#db.itproject.update({"bereich":{"$exists": True }}, {"$unset":{"bereich": ""}}, multi=True)
db.itproject.update({"bereich":{"$exists": True }}, {"$unset":{"bereich": ""}}, multi=True)
#db.itproject.update({"category":{"$exists": True }}, {"$unset":{"category": ""}}, multi=True)

      
#db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region.bundesland": [state, city]}}, multi=True)

for city in Baden_Württemberg:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, 
    {"$set":{"region.bundesland":"Baden-Wüttemburg", "region.stadt": city} }, multi=True)
#r'(?:[\s]|^)' + city '(?=[\s]|$)'
print(1)
for city in Bayern:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region.bundesland": "Bayern", "region.stadt": city}}, multi=True)
#print(len(BW))
print(2)
for city in Berlin:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region.bundesland": "Berlin", "region.stadt": city}}, multi=True)
#for state in location[0]:
print(3)
for city in Brandenburg:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region.bundesland": "Brandenburg", "region.stadt": city}}, multi=True)
#print(len(state))
print(4)
for city in Bremen:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region.bundesland": "Bremen", "region.stadt": city}}, multi=True)
print(5)       
#db.itproject.update({"location":{"$regex": '^.*' + city,"$options": 'i' }}, {"$set":{"region.bundesland": [state, "region.stadt": city}}, multi=True)
for city in Hamburg:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region.bundesland": "Hamburg", "region.stadt": city}}, multi=True)
#
print(6)
for city in Hessen:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region.bundesland": "Hessen", "region.stadt": city}}, multi=True)
#
print(7)
for city in Mecklenburg_Vorpommern:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region.bundesland": "Mecklenburg-Vorpommern", "region.stadt": city}}, multi=True)
#
print(8)
for city in Niedersachsen:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region.bundesland": "Niedersachsen", "region.stadt": city}}, multi=True)
#
print(9)
for city in Nordrhein_Westfalen:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region.bundesland": "Nordrhein-Westfalen", "region.stadt": city}}, multi=True)
#
print(10)
for city in Rheinland_Pfalz:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region.bundesland": "Rheinland-Pfalz", "region.stadt": city}}, multi=True)
#
print(11)
for city in Saarland:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region.bundesland": "Saarland", "region.stadt": city}}, multi=True)
#
print(12)
for city in Sachsen:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region.bundesland": "Sachsen", "region.stadt": city}}, multi=True)
#
print(13)
for city in Sachsen_Anhalt:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region.bundesland": "Sachsen-Anhalt", "region.stadt": city}}, multi=True)
#
print(14)
for city in Schleswig_Holstein:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region.bundesland": "Schleswig-Holstein", "region.stadt": city}}, multi=True)
#
print(15)
for city in Thüringen:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region.bundesland": "Thüringen", "region.stadt": city}}, multi=True)
print(16)
#db.itproject.update({ "$and": [ {"region.bundesland": None},{"location": {"$regex": '(baden|württ)', "$options": 'i'}}]}, {"$set":{"region.bundesland": "Baden Wüttemburg", "Baden Wüttem "region.stadt":burg"}}, multi=True)
for city in Ausland:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region.bundesland": "Ausland", "region.stadt": city}}, multi=True)
print(17)

#cisco
db.itproject.update({ "$and": [ {"bereich": None},{"title": {"$regex": '(cisco|ccna|ccnp|netzwerk)', "$options": 'i'}}, { "skill_summary": { "$regex": '(cisco|ccna|ccnp)', "$options": 'i' } }]}, 
{"$set":{"bereich.group": "Infrastructure", "bereich.type": "Netwerk Admin", "bereich.name": "CISCO"}}, multi=True)

db.itproject.update({ "$and": [ {"bereich": None},{"title": {"$regex": '(netzwerk|netzplan)', "$options": 'i'}}]}, 
{"$set":{"bereich.group": "Infrastructure", "bereich.type": "Netzwerk Admin", "bereich.name": "Others"}}, multi=True)

#devops
db.itproject.update({ "$and": [ {"bereich": None},{"title": {"$regex": '(devop|kuber|jenk)', "$options": 'i'}}, { "skill_summary": { "$not": re.compile('(^sap)') } }]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "DevOps"}}, multi=True)

#data science, bigdata
db.itproject.update({"$or": [{"category": {"$regex": '(Big Data|data|daten)', "$options": 'i'}}, {"title": {"$regex": '(Big Data|hadoop|spark)', "$options": 'i'}}]}, 
{"$set":{"bereich.group": "Data Science", "bereich.type":"Big Data"}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(big data|hadoop|spark)', "$options": 'i'} }, { "skill_summary": { "$not": re.compile('(^sap)') } }]}, 
{"$set":{"bereich.group": "Data Science", "bereich.type": "Big Data"}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "title": {"$regex": '(data scien|nlp|Regression|machine learning|tensorflow|tensor flow|^ml|datenanalyse|data analysis|daten analyse)', "$options": 'i'} }, { "skill_summary": { "$not": re.compile('(^sap)') } }]}, 
{"$set":{"bereich.group": "Data Science","bereich.type": "Machine Learning"}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "title": {"$regex": '(business inte|business anal|businessana)', "$options": 'i'} }, { "skill_summary": { "$not": re.compile('(^sap)') } }]}, 
{"$set":{"bereich.group": "Data Science","bereich.type": "Business Intelligence"}}, multi=True)

#mobile app
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(^ios|swift|objectiv)'} }, 
{ "skill_summary": {"$regex": '(^android|kotlin)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++|^js$|javascript|angular|vue|bootstrap|jquery)(?=[\s]|$)') } }]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Mobile", "bereich.platform": "Native", "bereich.platform_name": ["IOS", "Android"]}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(phonegap|ionic|cordova|flutter|react native)'} }, 
{ "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++|^js$|javascript|angular|vue|bootstrap|jquery)(?=[\s]|$)') } }]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Mobile", "bereich.platform": "Cross-Platform"}}, multi=True)

#fullstack skills with title
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": '(php|laravel)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap)'} } ], "title":{"$regex": '(php|Fullstack php|php Fullstack|laravel)', "$options": 'i'}}, 
{"$set":{"bereich.group": "Development",  "bereich.type": "Web", "bereich.stack":  "Fullstack","bereich.skill":  "PHP"}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(java|spring|j2ee|jvm)(?=[\s]|$)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|frontend)'} } ], "title":{"$regex": '(Java|Fullstack Java|Java Fullstack)', "$options": 'i'}}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Fullstack", "bereich.skill": "Java"}}, multi=True)

db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": '(node|express)'} }, { "skill_summary": {"$regex": '(react|angular|vue|css|express|html|bootstrap)'} } ], "title":{"$regex": '(php|Fullstack php|php Fullstack|laravel)', "$options": 'i'}}, 
{"$set":{"bereich.group": "Development",  "bereich.type": "Web", "bereich.stack": "Fullstack", "bereich.skill": "Nodejs"}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": '(python|django|flask|pyramid)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap)'} } ], "title":{"$regex": '(Python|Fullstack Python|Python Fullstack)', "$options": 'i'}},
{"$set":{"bereich.group": "Development",  "bereich.type": "Web", "bereich.stack": "Fullstack", "bereich.skill": "Python"}}, multi=True)

#sap bereich
db.itproject.update({ "$and": [ {"bereich": None},{"skill_summary": {"$regex": 'sap', "$options": 'i'}}]}, 
{"$set":{"bereich.group": "Infrastructure", "bereich.type": "ERP", "bereich.name": "SAP"}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{"title": {"$regex": r'(?:[\s]|^)(sap)(?=[\s]|$)', "$options": 'i'}}]}, 
{"$set":{"bereich.group": "Infrastructure", "bereich.type": "ERP", "bereich.name": "SAP"}}, multi=True)



#fullstack skills without title
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": '(ruby|rail)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ] }, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Fullstack", "bereich.skill": "Ruby & Rails"}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(java|spring|j2ee|jvm)(?=[\s]|$)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ] }, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Fullstack", "bereich.skill": "Java"}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": '(python|django|flask|pyramid)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ] }, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Fullstack", "bereich.skill": "Python"}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": '(php|laravel)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Fullstack", "bereich.skill": "PHP"}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": '(node|express)'} }, { "skill_summary": {"$regex": '(^js$|react|angular|vue|css|html|bootstrap|jquery|express|frontend)'} } ]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Fullstack", "bereich.skill": "Nodejs"}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(c|c\++)(?=[\s]|$)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery|express)'} } ]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Fullstack", "bereich.skill": "C/C++"}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(\.net|asp.net|c#|asp)(?=[\s]|$)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery|express)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|node.js|nodejs|c\++)(?=[\s]|$)') } } ]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Fullstack", "bereich.skill": "C#/ASP.Net"}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": '(backend)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery|frontend)'} } ] }, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Fullstack", "bereich.skill": "Others"}}, multi=True)


#frontend
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(^react)'} }, { "skill_summary": {"$regex": '(^angula)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++)(?=[\s]|$)') } }]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Frontend", "bereich.skill": "React & Angular"}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(^react)'} }, { "skill_summary": {"$regex": '(^vue)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++)(?=[\s]|$)') } }]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Frontend", "bereich.skill": "React & Vue"}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(^vue)'} }, { "skill_summary": {"$regex": '(^angula)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++)(?=[\s]|$)') } }]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Frontend", "bereich.skill": "Angular & Vue"}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(^react)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++)(?=[\s]|$)') } }]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Frontend", "bereich.skill": "React"}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(^angula)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++)(?=[\s]|$)') } }]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Frontend", "bereich.skill": "Angular"}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(^vue)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++)(?=[\s]|$)') } }]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Frontend", "bereich.skill": "Vue"}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(^js$|javascript|css|html|bootstrap|jquery|frontend)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++)(?=[\s]|$)') } }]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Frontend", "bereich.skill": "Others"}}, multi=True)

#backend
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(ruby|rail)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery)') } }]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Backend", "bereich.skill": "Ruby & Rails"}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(java|spring|j2ee|jvm)(?=[\s]|$)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery)') } }]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Backend", "bereich.skill": "Java"}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(python|django|flask|pyramid)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery)') } }]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Backend", "bereich.skill": "Python"}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(php|laravel)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery)') } }]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Backend", "bereich.skill": "PHP"}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(node|nodejs|node.js)(?=[\s]|$)'} }, { "skill_summary": { "$not": re.compile('(react|angular|vue|css|html|bootstrap|jquery)') } }]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Backend", "bereich.skill": "Nodejs"}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(c|c\++)(?=[\s]|$)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery)') } }]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Backend", "bereich.skill": "C/C++"}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(\.net|asp.net|c#|asp)(?=[\s]|$)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery)') } }]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Web", "bereich.stack": "Backend", "bereich.skill": "C#/Asp.Net"}}, multi=True)


#system admin
db.itproject.update({ "$and": [ {"bereich": None},{"title": {"$regex": '(system)', "$options": 'i'}}, {"skill_summary": {"$regex": '(linux)', "$options": 'i'}}]}, 
{"$set":{"bereich.group": "Infrastructure", "bereich.type": "System Admin", "bereich.name": "Linux"}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{"title": {"$regex": '(system|window|support)', "$options": 'i'}}, {"skill_summary": {"$regex": '(exchange|sql|windows|outlook|microsoft|admin)', "$options": 'i'}}]}, 
{"$set":{"bereich.group": "Infrastructure", "bereich.type": "System Admin", "bereich.name": "Microsoft"}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{"title": {"$regex": '(sharepoint)', "$options": 'i'}}]}, 
{"$set":{"bereich.group": "Infrastructure", "bereich.type": "System Admin", "bereich.name": "Microsoft/Sharepoint"}}, multi=True)

#IT Services
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(itil)', "$options": 'i'} }, { "skill_summary": { "$not": re.compile('(^sap)') } }]}, 
{"$set":{"bereich.group": "Infrastructure", "bereich.type": "IT Services", "bereich.name": "ITIL"}}, multi=True)

#saas
db.itproject.update({ "$and": [ {"bereich": None},{ "title": {"$regex": '(citrix)', "$options": 'i'} } ]}, 
{"$set":{"bereich.group": "Infrastructure", "bereich.type": "IT Services", "bereich.name": "CITRIX"}}, multi=True)
#oracle
db.itproject.update({ "$and": [ {"bereich": None},{ "title": {"$regex": '(oracle)', "$options": 'i'} } ]}, 
{"$set":{"bereich.group": "Infrastructure", "bereich.type": "IT Services", "bereich.name": "Oracle"}}, multi=True)


#Aggregate
pipeline = [{"$match": {"bereich": None}}, {"$out": "NoStack"}]
db.itproject.aggregate(pipeline)
pipeline1 = [{"$match": {"bereich": {"$ne": None}}}, {"$out": "itproject_clean"}]
db.itproject.aggregate(pipeline1)

#unset bereich
db.itproject.update({"bereich":{"$exists": True }}, {"$unset":{"bereich": ""}}, multi=True)
db.itproject.update({"region.bundesland":{"$exists": True }}, {"$unset":{"region.bundesland": ""}}, multi=True)
"""

#region.bundesland field with complicated location value
db.itproject.update({"location":{"$regex": '(^.*cologne|^.*koel|^.*koln|koe|cologne|koln)', "$options": 'i'}}, {"$set":{"region.bundesland": ["Nordrhein-Westfalen","Köln"]}}, multi=True)
db.itproject.update({"location":{"$regex": '(^.*duesseldorf|^.*dusseldorf|^.*dusse|duesseldorf|dusseldorf)', "$options": 'i'}}, {"$set":{"region.bundesland": [ "Nordrhein-Westfalen" ,"Düsseldorf"]}}, multi=True)
db.itproject.update({"location":{"$regex": '^DE', "$options": 'i'}}, {"$set":{"region.bundesland": ["Deutschland"]}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*Nuremberg', "$options": 'i'}}, {"$set":{"region.bundesland": [ "Bayern","Nüremberg"]}}, multi=True)
db.itproject.update({"location":{"$regex": '(^.*nrw|^.*nordrhein|nrw|nordrhein)', "$options": 'i'}}, {"$set":{"region.bundesland": ["Nordrhein-Westfalen", "Nordrhein-Westfalen"]}}, multi=True)
db.itproject.update({"location":{"$regex": '(^.*munich|^.*muenchen|^.*münchen|munich|muenchen|münich|^.*m&u)', "$options": 'i'}}, {"$set":{"region.bundesland": [ "Bayern","München"]}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*Sachsen', "$options": 'i'}}, {"$set":{"region.bundesland": ["Niedersachsen", "Niedersachsen"]}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*remote', "$options": 'i'}}, {"$set":{"region.bundesland": ["Remote"]}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*D-4', "$options": 'i'}}, {"$set":{"region.bundesland": ["D4"]}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*D-6', "$options": 'i'}}, {"$set":{"region.bundesland": ["D6"]}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*D-3', "$options": 'i'}}, {"$set":{"region.bundesland": ["D3"]}}, multi=True)
db.itproject.update({"location":{"$regex": 'CH|^.*Inter'}}, {"$set":{"region.bundesland": ["Ausland"]}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*kein', "$options": 'i'}}, {"$set":{"region.bundesland": ["None"]}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*hesse', "$options": 'i'}}, {"$set":{"region.bundesland": ["Hessen","Hessen"]}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*rheinland', "$options": 'i'}}, {"$set":{"region.bundesland": ["Rheinland-Pfalz", "Rheinland-Pfalz"]}}, multi=True)


#naming regions with locations not above
data = db.itproject.find({"region.bundesland": None })
for loc in data:
    a = loc['location']
    db.itproject.update({"region.bundesland": None}, {"$set":{"region.bundesland": [a]}})




#cisco
db.itproject.update({ "$and": [ {"bereich": None},{"title": {"$regex": '(cisco|ccna|ccnp|netzwerk)', "$options": 'i'}}, { "skill_summary": { "$regex": '(cisco|ccna|ccnp)', "$options": 'i' } }]}, {"$set":{"bereich": ["Netzwerk Administrator", "Cisco"]}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{"title": {"$regex": '(netzpla)', "$options": 'i'}}]}, {"$set":{"bereich": ["Netzwerk Administrator", "Telekommunikation"]}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{"title": {"$regex": '(netzwerk)', "$options": 'i'}}]}, {"$set":{"bereich": ["Netzwerk Administrator", "Others"]}}, multi=True)

#devops
db.itproject.update({ "$and": [ {"bereich": None},{"title": {"$regex": '(devop|kuber|jenk)', "$options": 'i'}}, { "skill_summary": { "$not": re.compile('(^sap)') } }]}, {"$set":{"bereich.group": "Development", "bereich.type": "DevOps"}}, multi=True)

#data science, bigdata
db.itproject.update({"$or": [{"category": {"$regex": '(Big Data|data|daten)', "$options": 'i'}}, {"title": {"$regex": '(Big Data|hadoop|spark)', "$options": 'i'}}]}, {"$set":{"bereich.group": "Data Science", "bereich.type":"Big Data"}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(big data|hadoop|spark)', "$options": 'i'} }, { "skill_summary": { "$not": re.compile('(^sap)') } }]}, {"$set":{"bereich.group": "Data Science", "bereich.type": "Big Data"}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "title": {"$regex": '(data scien|nlp|Regression|machine learning|tensorflow|tensor flow|^ml|datenanalyse|data analysis|daten analyse)', "$options": 'i'} }, { "skill_summary": { "$not": re.compile('(^sap)') } }]}, {"$set":{"bereich.group": "Data Science","bereich.type": "Machine Learning"}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "title": {"$regex": '(business inte|business anal|businessana)', "$options": 'i'} }, { "skill_summary": { "$not": re.compile('(^sap)') } }]}, {"$set":{"bereich.group": "Data Science","bereich.type": "Business Intelligence"}}, multi=True)




#fullstack skills with title
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": '(php|laravel)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ], "title":{"$regex": '(php|Fullstack php|php Fullstack|laravel)', "$options": 'i'}}, 
{"$set":{"bereich.group": "Development", "bereich.stack":  "Fullstack","bereich.skill":  "PHP"}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(java|spring|j2ee|jvm)(?=[\s]|$)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery|frontend)'} } ], "title":{"$regex": '(Java|Fullstack Java|Java Fullstack)', "$options": 'i'}}, 
{"$set":{"bereich.group": "Development", "bereich.stack": "Fullstack", "bereich.skill": "Java"}}, multi=True)

db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": '(node|express)'} }, { "skill_summary": {"$regex": '(react|angular|vue|css|express|html|bootstrap|jquery)'} } ], "title":{"$regex": '(php|Fullstack php|php Fullstack|laravel)', "$options": 'i'}}, {"$set":{"bereich.group": "Development", "bereich.stack": "Fullstack", "bereich.skill": "Nodejs"}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": '(python|django|flask|pyramid)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ], "title":{"$regex": '(Python|Fullstack Python|Python Fullstack)', "$options": 'i'}}, {"$set":{"bereich.group": "Development", "bereich.stack": "Fullstack", "bereich.skill": "Python"}}, multi=True)


#sap bereich
db.itproject.update({ "$and": [ {"bereich": None},{"skill_summary": {"$regex": 'sap', "$options": 'i'}}]}, {"$set":{"bereich.group": "SAP", "bereich.type"}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{"title": {"$regex": r'(?:[\s]|^)(sap)(?=[\s]|$)', "$options": 'i'}}]}, {"$set":{"bereich.group": "SAP", "bereich.type"}}, multi=True)



#fullstack skills without title
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": '(ruby|rail)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ] }, {"$set":{"bereich": ["Fullstack", "Ruby"]}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(java|spring|j2ee|jvm)(?=[\s]|$)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ] }, {"$set":{"bereich": ["Fullstack", "Java"]}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": '(python|django|flask|pyramid)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ] }, {"$set":{"bereich": ["Fullstack", "Python"]}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": '(php|laravel)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ]}, {"$set":{"bereich": ["Fullstack", "PHP"]}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": '(node|express)'} }, { "skill_summary": {"$regex": '(^js$|react|angular|vue|css|html|bootstrap|jquery|express|frontend)'} } ]}, {"$set":{"bereich": ["Fullstack", "Nodejs"]}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(c|c\++)(?=[\s]|$)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery|express)'} } ]}, {"$set":{"bereich": ["Fullstack", "C", "C++"]}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(\.net|asp.net|c#|asp)(?=[\s]|$)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery|express)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|node.js|nodejs|c\++)(?=[\s]|$)') } } ]}, {"$set":{"bereich": ["Fullstack", "C#", "Asp.net"]}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{ "skill_summary": {"$regex": '(backend)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery|frontend)'} } ] }, {"$set":{"bereich": ["Fullstack", "Any"]}}, multi=True)


#frontend
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(^react)'} }, { "skill_summary": {"$regex": '(^angula)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++)(?=[\s]|$)') } }]}, {"$set":{"bereich": ["Frontend", "React", "Angular"]}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(^react)'} }, { "skill_summary": {"$regex": '(^vue)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++)(?=[\s]|$)') } }]}, {"$set":{"bereich": ["Frontend", "React", "Vue"]}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(^vue)'} }, { "skill_summary": {"$regex": '(^angula)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++)(?=[\s]|$)') } }]}, {"$set":{"bereich": ["Frontend", "React", "Angular"]}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(^react)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++)(?=[\s]|$)') } }]}, {"$set":{"bereich": ["Frontend", "React"]}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(^angula)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++)(?=[\s]|$)') } }]}, {"$set":{"bereich": ["Frontend", "Angular"]}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(^vue)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++)(?=[\s]|$)') } }]}, {"$set":{"bereich": ["Frontend", "Vue"]}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(^js$|javascript|css|html|bootstrap|jquery|frontend)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++)(?=[\s]|$)') } }]}, {"$set":{"bereich": ["Frontend"]}}, multi=True)

#backend
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(ruby|rail)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery)') } }]}, {"$set":{"bereich": ["Backend", "Ruby"]}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(java|spring|j2ee|jvm)(?=[\s]|$)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery)') } }]}, {"$set":{"bereich": ["Backend", "Java"]}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(python|django|flask|pyramid)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery)') } }]}, {"$set":{"bereich": ["Backend", "Python"]}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(php|laravel)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery)') } }]}, {"$set":{"bereich": ["Backend", "PHP"]}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(node|nodejs|node.js)(?=[\s]|$)'} }, { "skill_summary": { "$not": re.compile('(react|angular|vue|css|html|bootstrap|jquery)') } }]}, {"$set":{"bereich": ["Backend", "Nodejs"]}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(c|c\++)(?=[\s]|$)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery)') } }]}, {"$set":{"bereich": ["Backend", "C", "C++"]}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(\.net|asp.net|c#|asp)(?=[\s]|$)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery)') } }]}, {"$set":{"bereich": ["Backend", "C#", "Asp.net"]}}, multi=True)


#system admin
db.itproject.update({ "$and": [ {"bereich": None},{"title": {"$regex": '(system)', "$options": 'i'}}, {"skill_summary": {"$regex": '(linux)', "$options": 'i'}}]}, {"$set":{"bereich": ["System Administrator", "Linux"]}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{"title": {"$regex": '(system|window|support)', "$options": 'i'}}, {"skill_summary": {"$regex": '(exchange|sql|windows|outlook|microsoft|admin)', "$options": 'i'}}]}, {"$set":{"bereich": ["System Administrator", "Microsoft"]}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{"title": {"$regex": '(sharepoint)', "$options": 'i'}}]}, {"$set":{"bereich": ["System Administrator", "Microsoft", "Sharepoint"]}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{"skill_summary": {"$regex": '(sharepoint)', "$options": 'i'}}]}, {"$set":{"bereich": ["System Administrator", "Microsoft", "Sharepoint"]}}, multi=True)
#IT support
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(itil)', "$options": 'i'} }, { "skill_summary": { "$not": re.compile('(^sap)') } }]}, {"$set":{"bereich": ["IT", "Service Management"]}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "title": {"$regex": '(oracle)', "$options": 'i'} }, { "skill_summary": { "$not": re.compile('(^sap)') } }]}, {"$set":{"bereich": ["IT", "Oracle Administrator"]}}, multi=True)
#java titles
db.itproject.update({ "$and": [ {"bereich": None},{ "title": {"$regex": r'(?:[\s]|^)(java|spring|j2ee|jvm|Java)(?=[\s]|$)'} } ]}, {"$set":{"bereich": ["Fullstack", "Java"]}}, multi=True)
#saas
db.itproject.update({ "$and": [ {"bereich": None},{ "title": {"$regex": '(citrix)', "$options": 'i'} } ]}, {"$set":{"bereich": ["Saas", "Citrix"]}}, multi=True)



#Aggregate
pipeline = [{"$match": {"bereich": None}}, {"$out": "NoStack"}]
db.itproject.aggregate(pipeline)
pipeline1 = [{"$match": {"bereich": {"$ne": None}}}, {"$out": "itproject_clean"}]
db.itproject.aggregate(pipeline1)

#unset bereich
db.itproject.update({"bereich":{"$exists": True }}, {"$unset":{"bereich": ""}}, multi=True)
db.itproject.update({"region.bundesland":{"$exists": True }}, {"$unset":{"region.bundesland": ""}}, multi=True)"""



























"""
#mobile app
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(^ios|swift|objectiv)'} }, 
{ "skill_summary": {"$regex": '(^android|kotlin)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++|^js$|javascript|angular|vue|bootstrap|jquery)(?=[\s]|$)') } }]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Mobile Apps", "bereich.platform": "Native", "bereich.platform_name": ["IOS", "Android"]}}, multi=True)
db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(phonegap|ionic|cordova|flutter|react native)'} }, 
{ "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++|^js$|javascript|angular|vue|bootstrap|jquery)(?=[\s]|$)') } }]}, 
{"$set":{"bereich.group": "Development", "bereich.type": "Mobile Apps", "bereich.platform": "Cross-Platform"}}, multi=True)
#db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(^ios|swift|objectiv)'} }, { "skill_summary": {"$regex": '(^android|kotlin)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++|^js$|javascript|react|angular|vue|bootstrap|jquery)(?=[\s]|$)') } }]}, {"$set":{"bereich.group": "Development", "bereich.type": "Mobile Apps", "bereich.platform": "Native" "bereich.platform_name": ["IOS", "Android"]}}, multi=True)
#db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(^ios|swift|objectiv)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery|java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c#|node.js|nodejs)') } }]}, {"$set":{"bereich.group": "Mobile", "IOS", "Native"]}}, multi=True)
#db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(android|kotlin)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c#|node.js|nodejs)') } }]}, {"$set":{"bereich.group": "Mobile", "Android", "Native"]}}, multi=True)
#db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(phonegap|ionic|cordova|flutter)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c#|node)') } }]}, {"$set":{"bereich.group": "Mobile", "Cross Platform"]}}, multi=True)
#db.itproject.update({ "$and": [{"bereich": None},{ "skill_summary": {"$regex": '(react|react native)'} }, { "skill_summary": {"$regex": '(mobile)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery|)') } }]}, {"$set":{"bereich.group": "Mobile App", "Cross Platform"]}}, multi=True)




location = ["Frankfurt", "Köln", "Bonn", "München", "Hamburg", "Berlin", "Stuttgart", "Düsseldorf", "Nürnberg", "Bayern", "Hannover", "Hessen", "Niedersachsen", "Karlsruhe",
             "Wiesbaden", "Bremen", "Mannheim", "Kiel", "Essen", "Ingolstadt", "Braunschweig", "Friedrichshafen", 
              "Leverkusen", "Dortmund", "Sailauf", "Darmstadt", "Dresden", "Münster", "Aschaffenburg", "Leipzig",
              "Heidelberg", "Wolfsburg", "Ulm", "Heilbronn", "Bielefeld", "Mainz", "Potsdam", "Eschborn", "Oldenburg", "Ludwigsburg",
              "Zurich", "Kassel", "Ruhrgebiet", "Würzburg", "Bern", "Augsburg", "Wuppertal", "Wilhelmshaven", "Kerpen", "Regensburg", "Freiburg",
               "Reutlingen", "Tübingen", "Jena", "Osnabrück", "Ostwestafalen", "Erding", "Aachen", "Erlangen", "Chemnitz", "Neuss", "Koblenz", "Erfurt", "Ratingen",
               "Waldorf", "Bad Homburg", "Ravensburg", "Bochum", "Ludwigshafen", "Duisburg", "Dachau", "Marburg", "Lübeck", "Gießen", "Pforzheim", "Leinfelden", "Gütersloh",
               "Saarbrücken", "Esslingen", "Offenbach", "Göttingen", "Cottbus", "Coburg", "Sindelfingen", "Sassenberg", "Halle", "Zwickau", "Göppingen", "Basel",
               "Ottobrunn", "Paderborn", "Remscheid", "Sankt Leon-Rot", "Amberg", "Montabaur", "Kaiserslautern", "Biberach", "Hamm", "Oberursel",  "Weinheim", "Gelsenkirchen", "Aalen", "Würzburg", "Ditzingen", "Hanau", "Melsungen",
               "Turgi", "Flensburg",  "Oberhausen", "Schwaben", "Aßlar", "Lindau", "Aurich", "Karlsfeld", "Kenzingen", "Künzelsau", "Schwerin", "Rastatt", "Passau", "Poing", "Schopfloch", "Elmshorn", 
               "Tuttlingen", "Magedeburg", "Hüttenberg", "Lohfelden", "Meckenheim", "Loßburg", "Rosenheim", "Gilching", "Germersheim", "Rastede", "Leichlingen", "Höchberg", "Bamberg", "Saarland", "Hilden", "Borken", "Bayreuth", "Heppenheim", "Mülheim", "Crailsheim", 
               "Böblingen",  "Kempten", "Sossenheim", "Weissach", "Lahr", "Vechta", "Bischofsheim", "Konstanz", "Warstein", "Genthin", "Dreilinden", "Brandenburg", "Husum", "Spelle", "Rheine", "Meerbusch", "Münzenberg", "Luterbach", "Herzogenaurach", "Siegen", "Ahrensburg",
               "Herne", "Eschwege", "Bottrop", "Cadolzburg", "Minden", "Kroppach", "Meschede", "Gummersbach", "Rimpar", "Oberpfalz", "Philippsburg", "Steinhausen", "Willich", "Offenburg", "Nordrhein-Westfalen", "D7", "D6", "D8", "D3", "D9", "D5", "D2","D0","D4","D1",'Baden-Württemberg', "Krefeld",
                'Rheinland-Pfalz', 'Rhein-Main-Gebiet','Schleswig-Holstein','Ostwestfalen', "Neckar", "Leon", 'Fürth', "Solingen", "None"]


location = [Baden_Württemberg, Bayern, Berlin, Brandenburg, Bremen, Hamburg, Hessen, Mecklenburg_Vorpommern, Niedersachsen, Nordrhein_Westfalen, Rheinland_Pfalz, Saarland, Sachsen, Sachsen_Anhalt, Schleswig_Holstein, Thüringen]
#add region.bundesland field using location value
germany = {'Baden_Württemberg': Baden_Württemberg,'Bayern': Bayern,'Berlin': Berlin, "Brandenburg": Brandenburg, 
         "Bremen": Bremen, "Hamburg": Hamburg, "Hessen": Hessen, "Mecklenburg_Vorpommern": Mecklenburg_Vorpommern,
         "Niedersachsen": Niedersachsen, "Nordrhein_Westfalen": Nordrhein_Westfalen, "Rheinland_Pfalz": Rheinland_Pfalz, 
         "Saarland": Saarland, "Sachsen": Sachsen, "Sachsen_Anhalt": Sachsen_Anhalt, "Schleswig_Holstein": Schleswig_Holstein, 
         "Thüringen": Thüringen, "Ausland": Ausland}
#data = db.itproject.find()

for city in location:
    db.itproject.update({"location":{"$regex": '^.*' + city,"$options": 'i' }}, {"$set":{"region.bundesland": [city]}}, multi=True)

"""


#frontend
#db.itproject.update({ "$and": [ { "skill_summary": {"$regex": r'(?:[\s]|^)(java|spring|j2ee)(?=[\s]|$)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ] }, {"$set":{"bereich": ["Fullstack", "Java"]}}, multi=True)
#db.itproject.update({ "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} }, { "skill_summary": { "$nin": [ {"$regex": '(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap)', "$options": 'i'} ] } }, {"$set":{"bereich": ["Frontend"]}}, multi=True)

#db.itproject.update({ "$and": [{ "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|)(?=[\s]|$)') } }]}, {"$set":{"bereich": ["Frontend"]}}, multi=True)
#{ name: { $regex: /acme.*corp/, $options: 'i', $nin: [ 'acmeblahcorp' ] } }

#{ tags: { $nin: [ "appliances", "school" ] } }

#r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap)(?=[\s]|$)'



#{ "$not": re.compile("^p.*") }

#db.itproject.update({"location":{"$regex": r'(?:[\s]|^)(münchen)(?=[\s]|$)', "$options": 'i'}}, {"$set":{"region.bundesland": "München"}}, multi=True)

#db.itproject.update({"bereich":{"$exists": True }}, {"$unset":{"bereich": ""}}, multi=True)

#add project bereich
#(?:[\s]|^)(java|node|nodejs|or|python)(?=[\s]|$)
#{skill_summary: {$all: ['java', 'js']}, title: RegExp('Java|Fullstack Java|Java Fullstack')}
#Java = {"$regex": '(Java|Fullstack Java|Java Fullstack)', "$options": 'i'}, {"$set":{"bereich": "Fullstack"}}


#db.itproject.update({"skill_summary":{"$regex": '(?:[\s]|^)(java)(?=[\s]|$)', "$options": 'i'}}, {"$set":{"bereich": "Java Developer"}}, multi=True)
#db.itproject.update({"skill_summary":{"$regex": 'react|angular|vue|jquery|frontend', "$options": 'm'}}, {"$set":{"bereich": "Frontend"}}, multi=True)

#db.itproject.update({"skill_summary":{"$regex": 'python|django|flask|nodejs|backend|spring|aws|docker|git|c#|java$', "$options": 'm'}}, {"$set":{"bereich": "Backend"}}, multi=True)

#db.itproject.update({"skill_summary":{"$regex": 'data|machine|science|natur|learning|lerne|analy|jupyter', "$options": 'm'}}, {"$set":{"bereich": "Data Science"}}, multi=True)

#db.itproject.update({"skill_summary":{"$regex": 'sap', "$options": 'i'}}, {"$set":{"bereich": "SAP"}}, multi=True)



"""frontEnd = ['javascript', 'html', 'css', 'jquery', 'html5', 'react', 'angular', 'vue', 'frontend' ]
backEnd = ['nodejs', 'python', 'java', 'php', 'go', 'flask', 'django', 'express', 'docker', 'backend', 'aws', 'git']
fullStack = [frontEnd, backEnd]
devOps = ['docker', 'kubernetes', 'ci', 'cd', 'jenkins', 'gitlab', 'devops', 'dev ops']
dscience = ['machine learning', 'data science', 'nlp', 'natural language', 'machine']
bigdata = ['hadoop', 'spark', 'bigdata', 'big data', 'aws', 'azure']
sap = ['sap']
db.itproject.update({"skill_summary":{"$regex": '', "$options": 'i'}}, {"$set":{"region.bundesland": "München"}}, multi=True)



#include this if you want to clean all fields
unknown = []
cleaned = []
for d in data:
    gen = d["location"]
    clean = re.sub(r'\W+', '', gen)
    unknown.append(gen)
    cleaned.append(clean)
    #db.itproject.update({"location":{"$regex": '^.*' + gen, "$options": 'i'}}, {"$set":{"location": clean}}, multi=True)
    #db.itproject.update({"location":{"$regex": '^.*' + clean, "$options": 'i'}}, {"$set":{"region.bundesland": clean}}, multi=True)
    #print(len(gen))
    #print(len(clean))



print(len(unknown))
print(len(cleaned))
for (u, c) in zip(unknown, cleaned):
    db.itproject.update({"location": u}, {"$set":{"region.bundesland": c}}, multi=True)"""
