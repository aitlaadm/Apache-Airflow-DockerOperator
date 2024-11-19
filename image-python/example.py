#!/usr/bin/env python
import pandas as pd
import json
# chargement des fichiers csv et converstion en dataframes
try:
    people_df = pd.read_csv('/opt/airflow/data/people.csv')
    places_df = pd.read_csv('/opt/airflow/data/places.csv')

    # jointure des df sur les colonnes city et place_of_birth
    merged_df = people_df.merge(places_df, left_on='place_of_birth', right_on='city', how='left')

    # Aggréation sur ountry et city avec 
    births_by_country = (merged_df.groupby('country')\
                        .size()\
                        .sort_values(ascending=False)\
                        .to_dict())

    # Ecriture du résultat dans le fichier json 
    try:
        with open('../data/total_births_by_country.json','w') as json_file:
            json.dump(births_by_country,json_file, separators=(',', ':'))
            print("Fichier total_births_by_country.json créé ")
    except IOError:
        print("Erreur d'écriture du fichier total_births_by_country.json")
        
except FileNotFoundError as e:
    print(f"Fichier non trouvé : {e}")
except pd.errors.EmptyDataError:
    print("Erreur: l'un des fichiers csv est vide")
except Exception as e:
    print("Erreur inattendue : {e}")


  

