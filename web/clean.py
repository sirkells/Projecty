from pymongo import MongoClient
import datetime
import re


def connect():
    connection = MongoClient('127.0.0.1', 27017)
    handle = connection["projectfinder"]
    return handle
db = connect()
data = db.itproject2.find({"region": None }) #None gets all doc without region field

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
               "Herne", "Eschwege", "Bottrop", "Cadolzburg", "Minden", "Kroppach", "Meschede", "Gummersbach", "Rimpar", "Oberpfalz", "Philippsburg", "Steinhausen", "Willich", "Offenburg", "Nordrhein-Westfalen", "D7", "D6", "D8", "D3", "D9", "D5", "D2","D0","D4","D1",'Baden-Württemberg', "Krefeld", "Deutschland",
               "CH",'Rheinland-Pfalz', 'Rhein-Main-Gebiet','Schleswig-Holstein','Ostwestfalen', "Neckar", "Leon", 'Fürth', "Solingen"]
for city in location:
    db.itproject2.update({"location":{"$regex": '^.*' + city,"$options": 'i' }}, {"$set":{"region": city}}, multi=True)
db.itproject2.update({"location":{"$regex": '^.*Munich', "$options": 'i'}}, {"$set":{"region": "München"}}, multi=True)
db.itproject2.update({"location":{"$regex": '^.*Muenchen', "$options": 'i'}}, {"$set":{"region": "München"}}, multi=True)
db.itproject2.update({"location":{"$regex": '^.*Cologne', "$options": 'i'}}, {"$set":{"region": "Köln"}}, multi=True)
db.itproject2.update({"location":{"$regex": '^.*Duesseldorf', "$options": 'i'}}, {"$set":{"region": "Düsseldorf"}}, multi=True)
db.itproject2.update({"location":{"$regex": '^.*Dusseldorf', "$options": 'i'}}, {"$set":{"region": "Düsseldorf"}}, multi=True)
db.itproject2.update({"location":{"$regex": '^.*DE', "$options": 'i'}}, {"$set":{"region": "Deutschland"}}, multi=True)
db.itproject2.update({"location":{"$regex": '^.*Nuremberg', "$options": 'i'}}, {"$set":{"region": "Nüremberg"}}, multi=True)
db.itproject2.update({"location":{"$regex": '^.*frankfurt', "$options": 'i'}}, {"$set":{"region": "Frankfurt"}}, multi=True)
db.itproject2.update({"location":{"$regex": '^.*Sachsen', "$options": 'i'}}, {"$set":{"region": "Niedersachsen"}}, multi=True)
db.itproject2.update({"location":{"$regex": '^.*NRW', "$options": 'i'}}, {"$set":{"region": "Nordrhein-Westfalen"}}, multi=True)
db.itproject2.update({"location":{"$regex": '^.*Nordrhein', "$options": 'i'}}, {"$set":{"region": "Nordrhein-Westfalen"}}, multi=True)
db.itproject2.update({"location":{"$regex": '^.*remote', "$options": 'i'}}, {"$set":{"region": "Remote"}}, multi=True)
db.itproject2.update({"location":{"$regex": '^.*D-4', "$options": 'i'}}, {"$set":{"region": "D4"}}, multi=True)
db.itproject2.update({"location":{"$regex": '^.*D-6', "$options": 'i'}}, {"$set":{"region": "D6"}}, multi=True)
db.itproject2.update({"location":{"$regex": '^.*D-3', "$options": 'i'}}, {"$set":{"region": "D3"}}, multi=True)
db.itproject2.update({"location":{"$regex": '^.*m&u', "$options": 'i'}}, {"$set":{"region": "München"}}, multi=True)
db.itproject2.update({"location":{"$regex": '^.*Inter', "$options": 'i'}}, {"$set":{"region": "Intl"}}, multi=True)
db.itproject2.update({"location":{"$regex": '^.*kein', "$options": 'i'}}, {"$set":{"region": "None"}}, multi=True)
db.itproject2.update({"location":{"$regex": '^.*hesse', "$options": 'i'}}, {"$set":{"region": "Hessen"}}, multi=True)




unknown = []
cleaned = []
for d in data:
    gen = d["location"]
    clean = re.sub(r'\W+', '', gen)
    unknown.append(gen)
    cleaned.append(clean)
    #db.itproject2.update({"location":{"$regex": '^.*' + gen, "$options": 'i'}}, {"$set":{"location": clean}}, multi=True)
    #db.itproject2.update({"location":{"$regex": '^.*' + clean, "$options": 'i'}}, {"$set":{"region": clean}}, multi=True)
    #print(len(gen))
    #print(len(clean))



print(len(unknown))
print(len(cleaned))
for (u, c) in zip(unknown, cleaned):
    db.itproject2.update({"location": u}, {"$set":{"region": c}}, multi=True)
