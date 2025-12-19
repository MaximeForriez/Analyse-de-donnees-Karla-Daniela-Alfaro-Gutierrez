#coding:utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Source des données : https://www.data.gouv.fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/
# Sources des données : production de M. Forriez, 2016-2023*

with open("data/resultats-elections-presidentielles-2022-1er-tour.csv", encoding="utf-8") as fichier:
    contenu = pd.read_csv(fichier)

#Question 5 : Les colonnes à caractères quantitatifs
print("5.Calcul des paramètres statistiques pour les colonnes quantitatives :") 

colonnes_quantitatives = [col for col in contenu.columns if contenu[col].dtype in ['int64', 'float64']] #valeur quantitatives avec/sans décimales
moyennes = [] #listes
medianes = []
modes = []
ecarts_types = []
ecarts_absolus = []
etendues = []

for col in colonnes_quantitatives:
    data = contenu[col].dropna()

    moy = data.mean()#moyenne
    moyennes.append(moy)

    med = data.median()#médiane
    medianes.append(med)
    
    mode_val = data.mode()#mode 
    if not mode_val.empty:
        modes.append(mode_val.iloc[0])
    else:
        modes.append(np.nan)
    
    ecart = data.std()#écart-type
    ecarts_types.append(ecart)
    
    ecart_abs = np.abs(data - moy).mean()
    ecarts_absolus.append(ecart_abs)
    
    etendue = data.max() - data.min()#étendue
    etendues.append(etendue)

stats = pd.DataFrame({
    "Colonne": colonnes_quantitatives,
    "Moyenne": moyennes,
    "Médiane": medianes,
    "Mode": modes,
    "Ecart-type": ecarts_types,
    "Ecart absolu moy": ecarts_absolus,
    "Etendue": etendues
})
stats = stats.round(2) #arrondir à 2 décimal max
print(stats)

#Question 6 : Liste de paramètres 
print("6.Liste des paramètres statistiques calculés :")

print(list(stats.columns))

#Question 7 : distance quartile et interdécile 
print("7.Calcul de l'IQR et de l'IDR :")

iqr = [] #quartile
idr = [] #décile 

for col in colonnes_quantitatives:
    data = contenu[col].dropna()

    q1 = data.quantile(0.25) #25% - quartiles
    q3 = data.quantile(0.75)
    iqr.append(q3 - q1)

    d1 = data.quantile(0.1)#10% - #décile
    d9 = data.quantile(0.9)
    idr.append(d9 - d1)

stats['IQR'] = iqr
stats['IDR'] = idr

print(stats.round(2))

#Question 8 : boîte à moustache 

for col in colonnes_quantitatives:
    data = contenu[col].dropna()
    plt.figure(figsize=(6,6))
    plt.boxplot(data)
    plt.title(f"Boîte à moustache - {col}")
    plt.ylabel("Valeurs")
    plt.savefig(f"img/boxplot_{col}.png") #choisir l'emplacement
    plt.close()

#Question 9
print("Lecture du fichier island-index.csv :")

with open ("data/island-index.csv", encoding= "utf-8") as fichier2:
    contenu = pd.read_csv(fichier2, low_memory=False) 
print(contenu)

#question 10 : nombres d'îles/superficie 
print("Nombre d'îles par catégorie de superficie :")

contenu["Surface (km²)"] = pd.to_numeric(contenu["Surface (km²)"], errors='coerce')#
surface = contenu["Surface (km²)"].dropna() #sélection de la colonne 
bins = [0, 10, 25, 50, 100, 2500, 5000, 10000, float('inf')]
labels = ("0-10", "10-25","25-50","50-100", "100-2500", "2500-5000","5000-10000", "10000+")
categories = pd.cut(surface, bins=bins, labels=labels, right=True, include_lowest=True)
compte = categories.value_counts().sort_index()
print(compte)

#organigramme
#DEBUT 
#Convertir "Surface (km²)" en numérique (erreurs → NaN)
#Supprimer les valeurs manquantes (dropna)
#Définir les classes de superficie (bins) + étiquettes (labels)
#Classer chaque île dans une classe (pd.cut)
#Compter le nombre d’îles par classe (value_counts) + trier (sort_index)
#Afficher les effectifs
# FIN