import csv

def top5(dico):
    return sorted(dico.items(), key=lambda x: x[1], reverse=True)[:5] # Fonction qui renvoie pour un dictionnaire les 5 valeurs les plus grand de la deuxième partie du tuple (a,b) où b est la partie qui nous interesse

names = ["User-ID", "Game title", "Behavior", "Value"]
purchases = {}   # Dictionnaire pour compter les achats
playtime = {}    # Dictionnaire pour additionner les heures de jeu

with open("steam-200k.csv", "r", encoding="utf-8") as fichier:
    reader = csv.DictReader(fichier, fieldnames=names)
    
    for row in (reader):
        title = row["Game title"].strip() # On utilise le .strip afin de ne pas se retrouver avec des espaces cachés pour éviter les doublons ou des erreurs lors de la conversion en float.
        behavior = row["Behavior"].strip() 
        value = row["Value"].strip() 
        try:
            value = float(row["Value"])
        except ValueError:
            value = 0.0

        if behavior == "purchase": # Ajoute 1 à l'achat du jeu ou initialise à 1 s'il n'existe pas
            if title in purchases:
                purchases[title] += 1
            else:
                purchases[title] = 1

        elif behavior == "play":   # Ajoute le playtime au jeu ciblé ou l'initialise à playtime s'il n'existe pas
            if title in playtime:
                playtime[title] += value
            else:
                playtime[title] = value


sorted_purchases = top5(purchases)
sorted_playtime = top5(playtime)


print("Top 5 des jeux les plus achetés:")
for title, count in sorted_purchases:
    print(f"{title} : {count} achats")

print("Top 5 des jeux les plus joués :")
for title, total_time in sorted_playtime:
    print(f"{title} : {total_time:.1f} heures")
