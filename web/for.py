from bundesland import Baden_Württemberg, Bayern, Berlin, Brandenburg, Bremen, Hamburg, Hessen, Mecklenburg_Vorpommern, Niedersachsen, Nordrhein_Westfalen, Rheinland_Pfalz, Saarland, Sachsen, Sachsen_Anhalt, Schleswig_Holstein, Thüringen, Ausland
list1 = [Baden_Württemberg]
list2 = [Bayern]

my_dict = {'list1': list1, 'list2': list2}
text = "adelberg"
matching = [s for s in Baden_Württemberg if "adelberg" in s]
print(matching)
    