#!/bin/bash

# Créer les dossiers de l'architecture du projet
mkdir -p timer_app/{views,controllers,models,utils,data}

# Créer un fichier __init__.py dans chaque dossier pour les rendre des packages Python
touch timer_app/__init__.py
touch timer_app/views/__init__.py
touch timer_app/controllers/__init__.py
touch timer_app/models/__init__.py
touch timer_app/utils/__init__.py

# Créer un fichier CSV vide dans le dossier data
touch timer_app/data/times.csv

echo "Structure de projet créée avec succès."