#!/usr/bin/env python
import json
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from collections import defaultdict
import time

place_to_country={}
birth_counts=defaultdict(int)

try:
    engine = sqlalchemy.create_engine("mysql://user_dteng:cirilgroupt@database/db_dteng")
    connection = engine.connect()
    metadata = sqlalchemy.schema.MetaData(engine)
    print("Connexion à la base de données réussie")    
except SQLAlchemyError as e:
        print(f"Erreur de connexion à la base de données: {e}")

# make an ORM object to refer to the table
Places=   sqlalchemy.schema.Table('places', metadata, autoload=True, autoload_with=engine)
People=   sqlalchemy.schema.Table('people', metadata, autoload=True, autoload_with=engine)
    
#mapping du résultat de la requete de selection des colonne city et country de la table places
places_query=connection.execute(sqlalchemy.select([Places.c.city, Places.c.country]))
for row in places_query:
    place_to_country[row['city']]=row['country']
        
#mapping du résultat de la requete de selection du place_of_birth afin de compter les personnes né dans le meme pays
people_query=connection.execute(sqlalchemy.select([People.c.place_of_birth]))
for row in people_query:
    place_of_birth=row['place_of_birth']
    country_of_birth=place_to_country.get(place_of_birth)
        
    if country_of_birth:
        birth_counts[country_of_birth]+=1
            
#écriture du contenu du dictionnaire birth_counts dans le fichier json summary_output.json
try:
    with open('../data/summary_output.json','w') as json_file:
        json.dump(birth_counts, json_file, separators=(',', ':'))
    print("Fichier de résumé créé !")
except Exception as e:
    print(f"Impossible de créer le fichier json : {e}")
      