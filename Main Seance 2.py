#coding:utf8

import pandas as pd
import matplotlib.pyplot as plt

# Source des données : https://www.data.gouv.fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/
with open("data/resultats-elections-presidentielles-2022-1er-tour.csv", encoding="utf-8") as fichier:
    contenu = pd.read_csv(fichier)
    print(contenu)
    pd.DataFrame(contenu)

# Mettre dans un commentaire le numéro de la question
# Question 6 
nb_lignes= len(contenu)
nb_colonnes= len(contenu.columns)
print("nombre de lignes ;", nb_lignes)
print("nombre de colonnes : ", nb_colonnes)

#Question 7 : afficher le type de données
print(contenu.dtypes)

#Question 8 : afficher le nom des colonnes (1ere ligne)
print(contenu.head())
print(contenu.columns)

#Question 9 : Sélectionner des inscrits
inscrits = contenu ["Inscrits"]
print(inscrits)

#Question 10 : la somme totale des inscrits (boucles effectif de chaque colonne)

total_inscrits = inscrits.sum()
print("Nombre total d'inscrits", total_inscrits)

somme_colonnes=[] #liste pour stocker les noms

for col in contenu.columns:
    if contenu[col].dtype in ["int64", "float64"]:
        somme_colonnes.append(contenu[col].sum())
print(somme_colonnes)#boucles qu'avec les données quantitatives donc int64 (sans décimales) et flot64 (avec décimales)

for col in contenu.columns:
    if contenu[col].dtype in ["int64", "float64"]:
        print(col, ":", contenu[col].sum()) #boucles plus lisible


#Question 11 : Diagramme en barre nombre inscrits et votants / département (boucle)

for i in range(len(contenu)): #=>en haut = la boucle
    dept= contenu.loc[i, "Libellé du département"]
    inscrits = contenu.loc[i, "Inscrits"]
    votants = contenu.loc[i, "Votants"]
    plt.figure(figsize=(8,6)) #Le diagramme
    plt.bar(["Inscrits","Votants"], [inscrits, votants], color=['blue', 'red'])
    plt.title(f"{dept}")
    plt.ylabel("Nombre de personnes")
    plt.ticklabel_format(style='plain', axis='y')
    #Avoir les noms et pas les valeurs de matplotlib
    plt.savefig(f"{dept}.png")
    plt.close()

#Question 12 : diagramme circulaire votes blancs, nuls, votants, abstentions (boucle)

import os
os.makedirs("images_circulaires", exist_ok=True)

for i in range(len(contenu)): #la boucle pour département
    dept = contenu.loc[i, "Libellé du département"]
    blancs = contenu.loc[i, "Blancs"]
    nuls = contenu.loc[i, "Nuls"]
    votants = contenu.loc[i, "Votants"]
    abstention = contenu.loc[i, "Abstentions"]

    # les diff votes exprimés(donc, votants, blanc et les votes nuls)

    exprimés = votants - blancs - nuls

    valeurs = [blancs, nuls, exprimés, abstention]
    labels = ["Blancs", "Nuls", "Exprimés", "Abstention"]
    couleurs = ["lightgrey", "red", "green", "orange"]

    plt.figure(figsize=(8,6))
    plt.pie(valeurs, labels=labels, colors=couleurs, autopct='%1.1f%%', startangle=90) #Les % à afficher les % dans le graphique circulaire!
    plt.title(f"{dept}")

    #Sauvegarder
    plt.savefig(f"images_circulaires/ {dept}.png")
    plt.close()


#Question 13 : Histogramme

plt.figure(figsize=(8,5))
plt.hist(contenu ["Inscrits"], bins=20, density=True, edgecolor='black', color='skyblue')
plt.title("Histogramme du nombre d'inscrits")
plt.xlabel("Nombre d'inscrits")
plt.ylabel("Densité")
plt.grid(alpha=0.3)
plt.show()
