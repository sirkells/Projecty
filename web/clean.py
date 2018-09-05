from pymongo import MongoClient
import datetime
import re


def connect():
    connection = MongoClient('172.16.11.200', 27017)
    handle = connection["projectfinder"]
    return handle
db = connect()
#data = db.itproject.find({"region": None }) #None gets all doc without region field


#db.itproject.update({"region1":{"$exists": True }}, {"$unset":{"region1": ""}}, multi=True)
#unset stack
db.itproject.update({"region":{"$exists": True }}, {"$unset":{"region": ""}}, multi=True)
db.itproject.update({"stack":{"$exists": True }}, {"$unset":{"stack": ""}}, multi=True)

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
               "CH",'Rheinland-Pfalz', 'Rhein-Main-Gebiet','Schleswig-Holstein','Ostwestfalen', "Neckar", "Leon", 'Fürth', "Solingen", "None"]

#add region field using location value
for city in location:
    db.itproject.update({"location":{"$regex": '^.*' + city,"$options": 'i' }}, {"$set":{"region": city}}, multi=True)


#region field with complicated location value
db.itproject.update({"location":{"$regex": '^.*Munich', "$options": 'i'}}, {"$set":{"region": "München"}}, multi=True)

db.itproject.update({"location":{"$regex": '^.*Muenchen', "$options": 'i'}}, {"$set":{"region": "München"}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*Cologne', "$options": 'i'}}, {"$set":{"region": "Köln"}}, multi=True)
db.itproject.update({"location":{"$regex": '^koe', "$options": 'i'}}, {"$set":{"region": "Köln"}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*Duesseldorf', "$options": 'i'}}, {"$set":{"region": "Düsseldorf"}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*Dusseldorf', "$options": 'i'}}, {"$set":{"region": "Düsseldorf"}}, multi=True)
db.itproject.update({"location":{"$regex": '^DE', "$options": 'i'}}, {"$set":{"region": "Deutschland"}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*Nuremberg', "$options": 'i'}}, {"$set":{"region": "Nüremberg"}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*North', "$options": 'i'}}, {"$set":{"region": "Nordrhein-Westfalen"}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*Sachsen', "$options": 'i'}}, {"$set":{"region": "Niedersachsen"}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*NRW', "$options": 'i'}}, {"$set":{"region": "Nordrhein-Westfalen"}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*Nordrhein', "$options": 'i'}}, {"$set":{"region": "Nordrhein-Westfalen"}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*remote', "$options": 'i'}}, {"$set":{"region": "Remote"}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*D-4', "$options": 'i'}}, {"$set":{"region": "D4"}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*D-6', "$options": 'i'}}, {"$set":{"region": "D6"}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*D-3', "$options": 'i'}}, {"$set":{"region": "D3"}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*m&u', "$options": 'i'}}, {"$set":{"region": "München"}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*Inter', "$options": 'i'}}, {"$set":{"region": "Intl"}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*kein', "$options": 'i'}}, {"$set":{"region": "None"}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*hesse', "$options": 'i'}}, {"$set":{"region": "Hessen"}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*rheinland', "$options": 'i'}}, {"$set":{"region": "Rheinland-Pfalz"}}, multi=True)
db.itproject.update({"location":{"$regex": '^.*münchen', "$options": 'i'}}, {"$set":{"region": "München"}}, multi=True)

#naming regions with locations not above
data = db.itproject.find({"region": None })
for loc in data:
    a = loc['location']
    
    db.itproject.update({"region": None}, {"$set":{"region": a}})

#db.itproject.update({"location":{"$regex": r'(?:[\s]|^)(münchen)(?=[\s]|$)', "$options": 'i'}}, {"$set":{"region": "München"}}, multi=True)

#db.itproject.update({"stack":{"$exists": True }}, {"$unset":{"stack": ""}}, multi=True)

#add project stack
#(?:[\s]|^)(java|node|nodejs|or|python)(?=[\s]|$)
#{skill_summary: {$all: ['java', 'js']}, title: RegExp('Java|Fullstack Java|Java Fullstack')}
#Java = {"$regex": '(Java|Fullstack Java|Java Fullstack)', "$options": 'i'}, {"$set":{"stack": "Fullstack"}}


#skills with title
db.itproject.update({ "$and": [ { "skill_summary": {"$regex": '(python|django|flask|pyramid)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ], "title":{"$regex": '(Python|Fullstack Python|Python Fullstack)', "$options": 'i'}}, {"$set":{"stack": ["Fullstack", "Python"]}}, multi=True)
db.itproject.update({ "$and": [ { "skill_summary": {"$regex": r'(?:[\s]|^)(java|spring|j2ee)(?=[\s]|$)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ], "title":{"$regex": '(Java|Fullstack Java|Java Fullstack)', "$options": 'i'}}, {"$set":{"stack": ["Fullstack", "Java"]}}, multi=True)
db.itproject.update({ "$and": [ { "skill_summary": {"$regex": '(php|laravel)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ], "title":{"$regex": '(php|Fullstack php|php Fullstack|laravel)', "$options": 'i'}}, {"$set":{"stack": ["Fullstack", "PHP"]}}, multi=True)
db.itproject.update({ "$and": [ { "skill_summary": {"$regex": '(node|express)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|express|html|bootstrap|jquery)'} } ], "title":{"$regex": '(php|Fullstack php|php Fullstack|laravel)', "$options": 'i'}}, {"$set":{"stack": ["Fullstack", "Node"]}}, multi=True)
#sap stack
db.itproject.update({"skill_summary": {"$regex": 'sap', "$options": 'i'}}, {"$set":{"stack": ["SAP"]}}, multi=True)
db.itproject.update({"title": {"$regex": r'(?:[\s]|^)(sap)(?=[\s]|$)', "$options": 'i'}}, {"$set":{"stack": ["SAP"]}}, multi=True)
#skills without title
db.itproject.update({ "$and": [ { "skill_summary": {"$regex": r'(?:[\s]|^)(java|spring|j2ee)(?=[\s]|$)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ] }, {"$set":{"stack": ["Fullstack", "Java"]}}, multi=True)
db.itproject.update({ "$and": [ { "skill_summary": {"$regex": '(python|django|flask|pyramid)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ] }, {"$set":{"stack": ["Fullstack", "Python"]}}, multi=True)
db.itproject.update({ "$and": [ { "skill_summary": {"$regex": '(php|laravel)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery)'} } ]}, {"$set":{"stack": ["Fullstack", "PHP"]}}, multi=True)
db.itproject.update({ "$and": [ { "skill_summary": {"$regex": '(node|express)'} }, { "skill_summary": {"$regex": '(^js|javascript|react|angular|vue|css|html|bootstrap|jquery|express)'} } ]}, {"$set":{"stack": ["Fullstack", "Node"]}}, multi=True)




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
