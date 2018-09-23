from bundesland import Baden_Württemberg, Bayern, Berlin, Brandenburg, Bremen, Hamburg, Hessen, Mecklenburg_Vorpommern, Niedersachsen, Nordrhein_Westfalen, Rheinland_Pfalz, Saarland, Sachsen, Sachsen_Anhalt, Schleswig_Holstein, Thüringen, Ausland
list1 = [Baden_Württemberg]
list2 = [Bayern]

my_dict = {'list1': list1, 'list2': list2}
text = "adelberg"
matching = [s for s in my_dict.values() if "adelberg" in s]
print(matching)
#print(my_dict.values())


import itertools

COLORED_THINGS = {'blue': Bremen,
                  'yellow': Ausland,
                  'red': Berlin}


for color, things in COLORED_THINGS.items():
    for thing in things:
        try:
            print(color + ":" + thing)
        except KeyError:
            print("error")
   
#la = [(x, y) for x, y in COLORED_THINGS.items() for z in y]
"""for city in Baden_Württemberg:
    db.itproject.update({"location":{"$regex": r'(?:[\s]|^)' + city + '(?=[\s]|$)'}}, {"$set":{"region": ["Baden-Wüttemburg", city]}}, multi=True)"""