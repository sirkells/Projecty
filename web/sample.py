from pymongo import MongoClient
import datetime

def connect():
    connection = MongoClient('127.0.0.1', 27017)
    handle = connection["projectfinder"]
    return handle
db = connect()
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
               "Tuttlingen", "Magedeburg", "Hüttenberg", "Lohfelden", "Meckenheim", "Loßburg", "Rosenheim", "Gilching", "Germersheim", "Rastede", "Leichlingen", "Höchberg", "Bamberg", "Saarland", "Hilden", "Borken", "Bayreuth", "Heppenheim", "Mülheim",  ]
for city in location:
    db.itproject3.update({"location":{"$regex": '^.*' + city + '*', "$options": 'i'}}, {"$set":{"region": city}}, multi=True)
db.itproject3.update({"location":{"$regex": '^.*Munich*', "$options": 'i'}}, {"$set":{"region": "München"}}, multi=True)
db.itproject3.update({"location":{"$regex": '^.*Muenchen*', "$options": 'i'}}, {"$set":{"region": "München"}}, multi=True)
db.itproject3.update({"location":{"$regex": '^.*Cologne*', "$options": 'i'}}, {"$set":{"region": "Köln"}}, multi=True)
    