from pymongo import MongoClient
import datetime
import re
from bundesland import Baden_Württemberg, Bayern, Berlin, Brandenburg, Bremen, Hamburg, Hessen, Mecklenburg_Vorpommern, Niedersachsen, Nordrhein_Westfalen, Rheinland_Pfalz, Saarland, Sachsen, Sachsen_Anhalt, Schleswig_Holstein, Thüringen, Ausland

def connect():
    connection = MongoClient('127.0.0.1', 27017)
    handle = connection["projectfinder"]
    return handle
db = connect()
#data = db.itproject.find({"region": None }) #None gets all doc without region field


#db.itproject.update({"region1":{"$exists": True }}, {"$unset":{"region1": ""}}, multi=True)
#unset stack
#db.itproject.update({"region":{"$exists": True }}, {"$unset":{"region": ""}}, multi=True)
#db.itproject.update({"stack":{"$exists": True }}, {"$unset":{"stack": ""}}, multi=True)
db.itproject.update({"bereich":{"$exists": True }}, {"$unset":{"bereich": ""}}, multi=True)
#db.itproject.update({"category":{"$exists": True }}, {"$unset":{"category": ""}}, multi=True)

      
#db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region": [state, city]}}, multi=True)

for city in Baden_Württemberg:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, 
    {"$set":{"region.bundesland":"Baden-Wüttemburg", "region.stadt": city} }, multi=True)
#r'(?:[\s]|^)' + city '(?=[\s]|$)'
print(1)

db.itproject.update({ "$and": [ {"bereich": None},{"title": {"$regex": '(cisco|ccna|ccnp|netzwerk)', "$options": 'i'}},
{ "skill_summary": { "$regex": '(cisco|ccna|ccnp)', "$options": 'i' } }]}, {"$set":{"bereich.group": "Infrastructure", "bereich.type": "Netzwerk Administrator", "bereich.skill": "Cisco"}}, multi=True)
db.itproject.update({ "$and": [ {"bereich": None},{"title": {"$regex": '(netzpla|netzwerk|network)', "$options": 'i'}}]}, 
{"$set":{"bereich.group": "Infrastructure", "bereich.type": "Netzwerk Administrator", "bereich.skill": "Others"}}, multi=True)
"""
for city in Bayern:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region": ["Bayern", city]}}, multi=True)
#print(len(BW))
print(2)
for city in Berlin:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region": ["Berlin", city]}}, multi=True)
#for state in location[0]:
print(3)
for city in Brandenburg:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region": ["Brandenburg", city]}}, multi=True)
#print(len(state))
print(4)
for city in Bremen:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region": ["Bremen", city]}}, multi=True)
print(5)       
#db.itproject.update({"location":{"$regex": '^.*' + city,"$options": 'i' }}, {"$set":{"region": [state, city]}}, multi=True)
for city in Hamburg:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region": ["Hamburg", city]}}, multi=True)
#
print(6)
for city in Hessen:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region": ["Hessen", city]}}, multi=True)
#
print(7)
for city in Mecklenburg_Vorpommern:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region": ["Mecklenburg-Vorpommern", city]}}, multi=True)
#
print(8)
for city in Niedersachsen:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region": ["Niedersachsen", city]}}, multi=True)
#
print(9)
for city in Nordrhein_Westfalen:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region": ["Nordrhein-Westfalen", city]}}, multi=True)
#
print(10)
for city in Rheinland_Pfalz:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region": ["Rheinland-Pfalz", city]}}, multi=True)
#
print(11)
for city in Saarland:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region": ["Saarland", city]}}, multi=True)
#
print(12)
for city in Sachsen:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region": ["Sachsen", city]}}, multi=True)
#
print(13)
for city in Sachsen_Anhalt:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region": ["Sachsen-Anhalt", city]}}, multi=True)
#
print(14)
for city in Schleswig_Holstein:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region": ["Schleswig-Holstein", city]}}, multi=True)
#
print(15)
for city in Thüringen:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region": ["Thüringen", city]}}, multi=True)
print(16)
#db.itproject.update({ "$and": [ {"region": None},{"location": {"$regex": '(baden|württ)', "$options": 'i'}}]}, {"$set":{"region": ["Baden Wüttemburg", "Baden Wüttemburg"]}}, multi=True)
for city in Ausland:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region": ["Ausland", city]}}, multi=True)
print(17)


#region field with complicated location value
db.itproject.update({"location":{"$regex": '(^.*cologne|^.*koel|^.*koln|koe|cologne|koln)', "$options": 'i'}}, {"$set":{"region": ["Nordrhein-Westfalen","Köln"]}}, multi=True)
db.itproject.update({"location":{"$regex": '(^.*duesseldorf|^.*dusseldorf|^.*dusse|duesseldorf|dusseldorf)', "$options": 'i'}}, {"$set":{"region": [ "Nordrhein-Westfalen" ,"Düsseldorf"]}}, multi=True)
db.itproject.update({"location":{"$regex": '^DE', "$options": 'i'}}, {"$set":{"region": ["Deutschland"]}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*Nuremberg', "$options": 'i'}}, {"$set":{"region": [ "Bayern","Nüremberg"]}}, multi=True)
db.itproject.update({"location":{"$regex": '(^.*nrw|^.*nordrhein|nrw|nordrhein)', "$options": 'i'}}, {"$set":{"region": ["Nordrhein-Westfalen", "Nordrhein-Westfalen"]}}, multi=True)
db.itproject.update({"location":{"$regex": '(^.*munich|^.*muenchen|^.*münchen|munich|muenchen|münich|^.*m&u)', "$options": 'i'}}, {"$set":{"region": [ "Bayern","München"]}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*Sachsen', "$options": 'i'}}, {"$set":{"region": ["Niedersachsen", "Niedersachsen"]}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*remote', "$options": 'i'}}, {"$set":{"region": ["Remote"]}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*D-4', "$options": 'i'}}, {"$set":{"region": ["D4"]}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*D-6', "$options": 'i'}}, {"$set":{"region": ["D6"]}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*D-3', "$options": 'i'}}, {"$set":{"region": ["D3"]}}, multi=True)
db.itproject.update({"location":{"$regex": 'CH|^.*Inter'}}, {"$set":{"region": ["Ausland"]}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*kein', "$options": 'i'}}, {"$set":{"region": ["None"]}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*hesse', "$options": 'i'}}, {"$set":{"region": ["Hessen","Hessen"]}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*rheinland', "$options": 'i'}}, {"$set":{"region": ["Rheinland-Pfalz", "Rheinland-Pfalz"]}}, multi=True)


#naming regions with locations not above
data = db.itproject.find({"region": None })
for loc in data:
    a = loc['location']
    db.itproject.update({"region": None}, {"$set":{"region": [a]}})




#cisco
db.itproject.update({ "$and": [ {"stack": None},{"title": {"$regex": '(cisco|ccna|ccnp|netzwerk)', "$options": 'i'}}, { "skill_summary": { "$regex": '(cisco|ccna|ccnp)', "$options": 'i' } }]}, {"$set":{"stack": ["Netzwerk Administrator", "Cisco"]}}, multi=True)
db.itproject.update({ "$and": [ {"stack": None},{"title": {"$regex": '(netzpla)', "$options": 'i'}}]}, {"$set":{"stack": ["Netzwerk Administrator", "Telekommunikation"]}}, multi=True)
db.itproject.update({ "$and": [ {"stack": None},{"title": {"$regex": '(netzwerk)', "$options": 'i'}}]}, {"$set":{"stack": ["Netzwerk Administrator", "Others"]}}, multi=True)

#devops
db.itproject.update({ "$and": [ {"stack": None},{"title": {"$regex": '(devop|kuber|jenk)', "$options": 'i'}}, { "skill_summary": { "$not": re.compile('(^sap)') } }]}, {"$set":{"stack": "DevOps"}}, multi=True)

#data science, bigdata
db.itproject.update({"$or": [{"category": {"$regex": '(Big Data|data|daten)', "$options": 'i'}}, {"title": {"$regex": '(Big Data|hadoop|spark)', "$options": 'i'}}]}, {"$set":{"stack": ["Data Science", "Big Data"]}}, multi=True)
db.itproject.update({ "$and": [{"stack": None},{ "skill_summary": {"$regex": '(big data|hadoop|spark)', "$options": 'i'} }, { "skill_summary": { "$not": re.compile('(^sap)') } }]}, {"$set":{"stack": ["Data Science", "Big Data"]}}, multi=True)
db.itproject.update({ "$and": [{"stack": None},{ "title": {"$regex": '(data scien|nlp|Regression|machine learning|tensorflow|tensor flow|^ml|datenanalyse|data analysis|daten analyse)', "$options": 'i'} }, { "skill_summary": { "$not": re.compile('(^sap)') } }]}, {"$set":{"stack": ["Data Science", "Machine Learning"]}}, multi=True)
db.itproject.update({ "$and": [{"stack": None},{ "title": {"$regex": '(business inte|business anal|businessana)', "$options": 'i'} }, { "skill_summary": { "$not": re.compile('(^sap)') } }]}, {"$set":{"stack": ["Data Science", "Business Intelligence"]}}, multi=True)

#mobile app
db.itproject.update({ "$and": [{"stack": None},{ "skill_summary": {"$regex": '(^ios|swift|objectiv)'} }, { "skill_summary": {"$regex": '(^android|kotlin)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++|^js$|javascript|react|angular|vue|bootstrap|jquery)(?=[\s]|$)') } }]}, {"$set":{"stack": ["Mobile", "Native", "IOS", "Android"]}}, multi=True)
db.itproject.update({ "$and": [{"stack": None},{ "skill_summary": {"$regex": '(^ios|swift|objectiv)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery|java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c#|node.js|nodejs)') } }]}, {"$set":{"stack": ["Mobile", "IOS", "Native"]}}, multi=True)
db.itproject.update({ "$and": [{"stack": None},{ "skill_summary": {"$regex": '(android|kotlin)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c#|node.js|nodejs)') } }]}, {"$set":{"stack": ["Mobile", "Android", "Native"]}}, multi=True)
db.itproject.update({ "$and": [{"stack": None},{ "skill_summary": {"$regex": '(phonegap|ionic|cordova|flutter)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c#|node)') } }]}, {"$set":{"stack": ["Mobile", "Cross Platform"]}}, multi=True)
db.itproject.update({ "$and": [{"stack": None},{ "skill_summary": {"$regex": '(react|react native)'} }, { "skill_summary": {"$regex": '(mobile)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery|)') } }]}, {"$set":{"stack": ["Mobile App", "Cross Platform"]}}, multi=True)
#fullstack skills with title
db.itproject.update({ "$and": [ {"stack": None},{ "skill_summary": {"$regex": '(php|laravel)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ], "title":{"$regex": '(php|Fullstack php|php Fullstack|laravel)', "$options": 'i'}}, {"$set":{"stack": ["Fullstack", "PHP"]}}, multi=True)
db.itproject.update({ "$and": [ {"stack": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(java|spring|j2ee|jvm)(?=[\s]|$)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery|frontend)'} } ], "title":{"$regex": '(Java|Fullstack Java|Java Fullstack)', "$options": 'i'}}, {"$set":{"stack": ["Fullstack", "Java"]}}, multi=True)

db.itproject.update({ "$and": [ {"stack": None},{ "skill_summary": {"$regex": '(node|express)'} }, { "skill_summary": {"$regex": '(react|angular|vue|css|express|html|bootstrap|jquery)'} } ], "title":{"$regex": '(php|Fullstack php|php Fullstack|laravel)', "$options": 'i'}}, {"$set":{"stack": ["Fullstack", "Nodejs"]}}, multi=True)
db.itproject.update({ "$and": [ {"stack": None},{ "skill_summary": {"$regex": '(python|django|flask|pyramid)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ], "title":{"$regex": '(Python|Fullstack Python|Python Fullstack)', "$options": 'i'}}, {"$set":{"stack": ["Fullstack", "Python"]}}, multi=True)
#sap stack
db.itproject.update({ "$and": [ {"stack": None},{"skill_summary": {"$regex": 'sap', "$options": 'i'}}]}, {"$set":{"stack": ["SAP"]}}, multi=True)
db.itproject.update({ "$and": [ {"stack": None},{"title": {"$regex": r'(?:[\s]|^)(sap)(?=[\s]|$)', "$options": 'i'}}]}, {"$set":{"stack": ["SAP"]}}, multi=True)
#fullstack skills without title
db.itproject.update({ "$and": [ {"stack": None},{ "skill_summary": {"$regex": '(ruby|rail)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ] }, {"$set":{"stack": ["Fullstack", "Ruby"]}}, multi=True)
db.itproject.update({ "$and": [ {"stack": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(java|spring|j2ee|jvm)(?=[\s]|$)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ] }, {"$set":{"stack": ["Fullstack", "Java"]}}, multi=True)
db.itproject.update({ "$and": [ {"stack": None},{ "skill_summary": {"$regex": '(python|django|flask|pyramid)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ] }, {"$set":{"stack": ["Fullstack", "Python"]}}, multi=True)
db.itproject.update({ "$and": [ {"stack": None},{ "skill_summary": {"$regex": '(php|laravel)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ]}, {"$set":{"stack": ["Fullstack", "PHP"]}}, multi=True)
db.itproject.update({ "$and": [ {"stack": None},{ "skill_summary": {"$regex": '(node|express)'} }, { "skill_summary": {"$regex": '(^js$|react|angular|vue|css|html|bootstrap|jquery|express|frontend)'} } ]}, {"$set":{"stack": ["Fullstack", "Nodejs"]}}, multi=True)
db.itproject.update({ "$and": [ {"stack": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(c|c\++)(?=[\s]|$)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery|express)'} } ]}, {"$set":{"stack": ["Fullstack", "C", "C++"]}}, multi=True)
db.itproject.update({ "$and": [ {"stack": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(\.net|asp.net|c#|asp)(?=[\s]|$)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery|express)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|node.js|nodejs|c\++)(?=[\s]|$)') } } ]}, {"$set":{"stack": ["Fullstack", "C#", "Asp.net"]}}, multi=True)
db.itproject.update({ "$and": [ {"stack": None},{ "skill_summary": {"$regex": '(backend)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery|frontend)'} } ] }, {"$set":{"stack": ["Fullstack", "Any"]}}, multi=True)


#frontend
db.itproject.update({ "$and": [{"stack": None},{ "skill_summary": {"$regex": '(^react)'} }, { "skill_summary": {"$regex": '(^angula)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++)(?=[\s]|$)') } }]}, {"$set":{"stack": ["Frontend", "React", "Angular"]}}, multi=True)
db.itproject.update({ "$and": [{"stack": None},{ "skill_summary": {"$regex": '(^react)'} }, { "skill_summary": {"$regex": '(^vue)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++)(?=[\s]|$)') } }]}, {"$set":{"stack": ["Frontend", "React", "Vue"]}}, multi=True)
db.itproject.update({ "$and": [{"stack": None},{ "skill_summary": {"$regex": '(^vue)'} }, { "skill_summary": {"$regex": '(^angula)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++)(?=[\s]|$)') } }]}, {"$set":{"stack": ["Frontend", "React", "Angular"]}}, multi=True)
db.itproject.update({ "$and": [{"stack": None},{ "skill_summary": {"$regex": '(^react)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++)(?=[\s]|$)') } }]}, {"$set":{"stack": ["Frontend", "React"]}}, multi=True)
db.itproject.update({ "$and": [{"stack": None},{ "skill_summary": {"$regex": '(^angula)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++)(?=[\s]|$)') } }]}, {"$set":{"stack": ["Frontend", "Angular"]}}, multi=True)
db.itproject.update({ "$and": [{"stack": None},{ "skill_summary": {"$regex": '(^vue)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++)(?=[\s]|$)') } }]}, {"$set":{"stack": ["Frontend", "Vue"]}}, multi=True)
db.itproject.update({ "$and": [{"stack": None},{ "skill_summary": {"$regex": '(^js$|javascript|css|html|bootstrap|jquery|frontend)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|node.js|nodejs|c\++)(?=[\s]|$)') } }]}, {"$set":{"stack": ["Frontend"]}}, multi=True)

#backend
db.itproject.update({ "$and": [{"stack": None},{ "skill_summary": {"$regex": '(ruby|rail)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery)') } }]}, {"$set":{"stack": ["Backend", "Ruby"]}}, multi=True)
db.itproject.update({ "$and": [{"stack": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(java|spring|j2ee|jvm)(?=[\s]|$)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery)') } }]}, {"$set":{"stack": ["Backend", "Java"]}}, multi=True)
db.itproject.update({ "$and": [{"stack": None},{ "skill_summary": {"$regex": '(python|django|flask|pyramid)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery)') } }]}, {"$set":{"stack": ["Backend", "Python"]}}, multi=True)
db.itproject.update({ "$and": [{"stack": None},{ "skill_summary": {"$regex": '(php|laravel)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery)') } }]}, {"$set":{"stack": ["Backend", "PHP"]}}, multi=True)
db.itproject.update({ "$and": [{"stack": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(node|nodejs|node.js)(?=[\s]|$)'} }, { "skill_summary": { "$not": re.compile('(react|angular|vue|css|html|bootstrap|jquery)') } }]}, {"$set":{"stack": ["Backend", "Nodejs"]}}, multi=True)
db.itproject.update({ "$and": [{"stack": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(c|c\++)(?=[\s]|$)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery)') } }]}, {"$set":{"stack": ["Backend", "C", "C++"]}}, multi=True)
db.itproject.update({ "$and": [{"stack": None},{ "skill_summary": {"$regex": r'(?:[\s]|^)(\.net|asp.net|c#|asp)(?=[\s]|$)'} }, { "skill_summary": { "$not": re.compile('(^js$|javascript|react|angular|vue|css|html|bootstrap|jquery)') } }]}, {"$set":{"stack": ["Backend", "C#", "Asp.net"]}}, multi=True)


#system admin
db.itproject.update({ "$and": [ {"stack": None},{"title": {"$regex": '(system)', "$options": 'i'}}, {"skill_summary": {"$regex": '(linux)', "$options": 'i'}}]}, {"$set":{"stack": ["System Administrator", "Linux"]}}, multi=True)
db.itproject.update({ "$and": [ {"stack": None},{"title": {"$regex": '(system|window|support)', "$options": 'i'}}, {"skill_summary": {"$regex": '(exchange|sql|windows|outlook|microsoft|admin)', "$options": 'i'}}]}, {"$set":{"stack": ["System Administrator", "Microsoft"]}}, multi=True)
db.itproject.update({ "$and": [ {"stack": None},{"title": {"$regex": '(sharepoint)', "$options": 'i'}}]}, {"$set":{"stack": ["System Administrator", "Microsoft", "Sharepoint"]}}, multi=True)
db.itproject.update({ "$and": [ {"stack": None},{"skill_summary": {"$regex": '(sharepoint)', "$options": 'i'}}]}, {"$set":{"stack": ["System Administrator", "Microsoft", "Sharepoint"]}}, multi=True)
#IT support
db.itproject.update({ "$and": [{"stack": None},{ "skill_summary": {"$regex": '(itil)', "$options": 'i'} }, { "skill_summary": { "$not": re.compile('(^sap)') } }]}, {"$set":{"stack": ["IT", "Service Management"]}}, multi=True)
db.itproject.update({ "$and": [{"stack": None},{ "title": {"$regex": '(oracle)', "$options": 'i'} }, { "skill_summary": { "$not": re.compile('(^sap)') } }]}, {"$set":{"stack": ["IT", "Oracle Administrator"]}}, multi=True)
#java titles
db.itproject.update({ "$and": [ {"stack": None},{ "title": {"$regex": r'(?:[\s]|^)(java|spring|j2ee|jvm|Java)(?=[\s]|$)'} } ]}, {"$set":{"stack": ["Fullstack", "Java"]}}, multi=True)
#saas
db.itproject.update({ "$and": [ {"stack": None},{ "title": {"$regex": '(citrix)', "$options": 'i'} } ]}, {"$set":{"stack": ["Saas", "Citrix"]}}, multi=True)



#Aggregate
pipeline = [{"$match": {"stack": None}}, {"$out": "NoStack"}]
db.itproject.aggregate(pipeline)
pipeline1 = [{"$match": {"stack": {"$ne": None}}}, {"$out": "itproject_clean"}]
db.itproject.aggregate(pipeline1)

#unset stack
db.itproject.update({"stack":{"$exists": True }}, {"$unset":{"stack": ""}}, multi=True)
db.itproject.update({"region":{"$exists": True }}, {"$unset":{"region": ""}}, multi=True)"""



























"""location = ["Frankfurt", "Köln", "Bonn", "München", "Hamburg", "Berlin", "Stuttgart", "Düsseldorf", "Nürnberg", "Bayern", "Hannover", "Hessen", "Niedersachsen", "Karlsruhe",
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
#add region field using location value
germany = {'Baden_Württemberg': Baden_Württemberg,'Bayern': Bayern,'Berlin': Berlin, "Brandenburg": Brandenburg, 
         "Bremen": Bremen, "Hamburg": Hamburg, "Hessen": Hessen, "Mecklenburg_Vorpommern": Mecklenburg_Vorpommern,
         "Niedersachsen": Niedersachsen, "Nordrhein_Westfalen": Nordrhein_Westfalen, "Rheinland_Pfalz": Rheinland_Pfalz, 
         "Saarland": Saarland, "Sachsen": Sachsen, "Sachsen_Anhalt": Sachsen_Anhalt, "Schleswig_Holstein": Schleswig_Holstein, 
         "Thüringen": Thüringen, "Ausland": Ausland}
#data = db.itproject.find()

for city in location:
    db.itproject.update({"location":{"$regex": '^.*' + city,"$options": 'i' }}, {"$set":{"region": [city]}}, multi=True)

"""


#frontend
#db.itproject.update({ "$and": [ { "skill_summary": {"$regex": r'(?:[\s]|^)(java|spring|j2ee)(?=[\s]|$)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ] }, {"$set":{"stack": ["Fullstack", "Java"]}}, multi=True)
#db.itproject.update({ "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} }, { "skill_summary": { "$nin": [ {"$regex": '(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap)', "$options": 'i'} ] } }, {"$set":{"stack": ["Frontend"]}}, multi=True)

#db.itproject.update({ "$and": [{ "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} }, { "skill_summary": { "$not": re.compile(r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap|c|c#|)(?=[\s]|$)') } }]}, {"$set":{"stack": ["Frontend"]}}, multi=True)
#{ name: { $regex: /acme.*corp/, $options: 'i', $nin: [ 'acmeblahcorp' ] } }

#{ tags: { $nin: [ "appliances", "school" ] } }

#r'(?:[\s]|^)(java|spring|j2ee|python|django|flask|pyramid|php|laravel|node|express|sap)(?=[\s]|$)'



#{ "$not": re.compile("^p.*") }

#db.itproject.update({"location":{"$regex": r'(?:[\s]|^)(münchen)(?=[\s]|$)', "$options": 'i'}}, {"$set":{"region": "München"}}, multi=True)

#db.itproject.update({"stack":{"$exists": True }}, {"$unset":{"stack": ""}}, multi=True)

#add project stack
#(?:[\s]|^)(java|node|nodejs|or|python)(?=[\s]|$)
#{skill_summary: {$all: ['java', 'js']}, title: RegExp('Java|Fullstack Java|Java Fullstack')}
#Java = {"$regex": '(Java|Fullstack Java|Java Fullstack)', "$options": 'i'}, {"$set":{"stack": "Fullstack"}}


#db.itproject.update({"skill_summary":{"$regex": '(?:[\s]|^)(java)(?=[\s]|$)', "$options": 'i'}}, {"$set":{"stack": "Java Developer"}}, multi=True)
#db.itproject.update({"skill_summary":{"$regex": 'react|angular|vue|jquery|frontend', "$options": 'm'}}, {"$set":{"stack": "Frontend"}}, multi=True)

#db.itproject.update({"skill_summary":{"$regex": 'python|django|flask|nodejs|backend|spring|aws|docker|git|c#|java$', "$options": 'm'}}, {"$set":{"stack": "Backend"}}, multi=True)

#db.itproject.update({"skill_summary":{"$regex": 'data|machine|science|natur|learning|lerne|analy|jupyter', "$options": 'm'}}, {"$set":{"stack": "Data Science"}}, multi=True)

#db.itproject.update({"skill_summary":{"$regex": 'sap', "$options": 'i'}}, {"$set":{"stack": "SAP"}}, multi=True)



"""frontEnd = ['javascript', 'html', 'css', 'jquery', 'html5', 'react', 'angular', 'vue', 'frontend' ]
backEnd = ['nodejs', 'python', 'java', 'php', 'go', 'flask', 'django', 'express', 'docker', 'backend', 'aws', 'git']
fullStack = [frontEnd, backEnd]
devOps = ['docker', 'kubernetes', 'ci', 'cd', 'jenkins', 'gitlab', 'devops', 'dev ops']
dscience = ['machine learning', 'data science', 'nlp', 'natural language', 'machine']
bigdata = ['hadoop', 'spark', 'bigdata', 'big data', 'aws', 'azure']
sap = ['sap']
db.itproject.update({"skill_summary":{"$regex": '', "$options": 'i'}}, {"$set":{"region": "München"}}, multi=True)



#include this if you want to clean all fields
unknown = []
cleaned = []
for d in data:
    gen = d["location"]
    clean = re.sub(r'\W+', '', gen)
    unknown.append(gen)
    cleaned.append(clean)
    #db.itproject.update({"location":{"$regex": '^.*' + gen, "$options": 'i'}}, {"$set":{"location": clean}}, multi=True)
    #db.itproject.update({"location":{"$regex": '^.*' + clean, "$options": 'i'}}, {"$set":{"region": clean}}, multi=True)
    #print(len(gen))
    #print(len(clean))



print(len(unknown))
print(len(cleaned))
for (u, c) in zip(unknown, cleaned):
    db.itproject.update({"location": u}, {"$set":{"region": c}}, multi=True)"""
