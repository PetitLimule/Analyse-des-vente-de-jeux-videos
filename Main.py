import csv
import matplotlib.pyplot as plt

##################################################################
             # Définition des fonctions
##################################################################
def top5(dico):
    """
    Fonction qui renvoie pour un dictionnaire les 5 valeurs les plus grand de la deuxième partie du tuple (a,b) où b est la partie qui nous interesse
    """
    return sorted(dico.items(), key=lambda x: x[1], reverse=True)[:5] 

def format_ticks(axis, values):
    """
    Fonction qui formate l'axe X d'un graphique avec des unités lisibles (k, M)
    - axis : l'objet matplotlib (ex : axes[0] ou axes[1])
    - values : la liste de valeurs utilisées pour le graphique
    """
    max_value = max(values)
    step = max_value / 5  # environ 5 divisions sur l'axe
    ticks = [int(i * step) for i in range(6)]
    labels = []  # Conversion des nombres en texte lisible
    for val in ticks:
        if val >= 1_000_000:
            labels.append(f"{val/1_000_000:.2f}M")
        elif val >= 1_000:
            labels.append(f"{val/1_000:.1f}k")
        else:
            labels.append(str(val))
    axis.set_xticks(ticks)
    axis.set_xticklabels(labels)

##################################################################
                # Début du programme
##################################################################


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

# --- AFFICHAGE GRAPHIQUE ---
# On sépare les titres et les valeurs pour faciliter l’affichage
titles_purchases = [title for title, _ in sorted_purchases]
values_purchases = [count for _, count in sorted_purchases]

titles_playtime = [title for title, _ in sorted_playtime]
values_playtime = [time for _, time in sorted_playtime]

# Création d'une figure avec deux sous-graphiques côte à côte
fig, axes = plt.subplots(1, 2, figsize=(12, 5))  # 1 ligne, 2 colonnes

# Premier graphique : Achats
axes[0].barh(titles_purchases[::-1], values_purchases[::-1], color="skyblue")
axes[0].set_title("Top 5 - Jeux les plus achetés")
axes[0].set_ylabel("Jeu")
axes[0].set_xlabel("Nombre d'achats")
axes[0].set_xlim(0, max(values_purchases) * 1.15)
format_ticks(axes[0], values_purchases)
for i, v in enumerate(values_purchases[::-1]):
    display_val = f"{v/1000:.1f}k" if v >= 1000 else str(v)
    axes[0].text(v + max(values_purchases)*0.01, i, display_val, va='center', fontsize=10)


# Deuxième graphique : Temps de jeu
axes[1].barh(titles_playtime[::-1], values_playtime[::-1], color="lightgreen")
axes[1].set_title("Top 5 - Jeux les plus joués")
axes[1].set_ylabel("Jeu")
axes[1].set_xlabel("Heures totales")
axes[1].set_xlim(0, max(values_playtime) * 1.20)
format_ticks(axes[1], values_playtime)
for i, v in enumerate(values_playtime[::-1]):
    display_val = f"{v/1000:.1f}k" if v >= 1000 else str(v)
    axes[1].text(v + max(values_purchases)*0.01, i, display_val, va='center', fontsize=10)




plt.tight_layout()
plt.show()
