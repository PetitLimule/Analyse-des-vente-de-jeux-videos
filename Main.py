import csv

fichier = open('C:/Users/MAX/Documents/Github/Projet vente de jeux/steam-200k.csv','r',encoding=('UTF-8'))
sales=list(csv.DictReader(fichier))
print(sales[0])