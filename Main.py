import csv

fichier = open('steam-200k.csv','r',encoding=('UTF-8'))
sales=list(csv.DictReader(fichier))

print(sales[0])
