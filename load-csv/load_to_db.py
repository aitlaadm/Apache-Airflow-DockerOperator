#!/usr/bin/env python
import csv
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import time

# connection à la base de données

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

# insertion des lignes des fichiers dans les tables spécifiques
try:
  with open('/opt/airflow/data/people.csv') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)
    for row in reader: 
      connection.execute(People.insert().values(
        given_name = row[0],
        family_name=row[1],
        date_of_birth=row[2],
        place_of_birth=row[3]
        ))
except FileNotFoundError:
  print("Fichier people.csv introuvable.")
except SQLAlchemyError as e:
  print(f"Erreur d'insertion Table ""people"": {e}")
except Exception as e:
  print(f"Erreur : {e}")
    
try:
  with open('/opt/airflow/data/places.csv') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)
    for row in reader: 
      connection.execute(Places.insert().values(
        city = row[0],
        county=row[1],
        country=row[2]
        ))
      
except SQLAlchemyError as e:
  print(f"Erreur d'insertion dans la table ""places"": {e}")
except FileNotFoundError:
  print("Fichier places.csv introuvable.")
except Exception as e:
  print(f"Erreur : {e}")
   