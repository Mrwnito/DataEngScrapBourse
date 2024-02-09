# DataEngScrapBourse

# Projet Data Engineering : Visualisation des Indices Financiers

## Introduction

Ce projet consiste en une application web permettant de visualiser et comparer les performances de différents indices financiers, notamment le CAC 40, le SBF 120, le CAC 40 ESG et l'ENT PEA PME 150, au travers de graphiques interactifs.

## Fonctionnalités

- **Visualisation des Indices Financiers :** Affichage des performances historiques des indices financiers sélectionnés à travers des graphiques linéaires.
- **Comparaison des Performances :** Comparaison des changements en pourcentage des indices financiers sur une période donnée.
- **Interactivité :** Possibilité de survoler les graphiques pour voir les valeurs précises à différents points dans le temps.

## Technologie

Le projet est développé en utilisant :

- **Python 3.8** : Langage de programmation principal.
- **Flask** : Framework web utilisé pour construire l'application web.
- **Scrapy** : Framework utilisé pour extraire les données des indices financiers à partir de sources web.
- **MongoDB** : Base de données pour stocker les données extraites.
- **Docker** : Utilisé pour conteneuriser l'application et faciliter le déploiement.

## Structure du Projet

ProjetDataEng/
├── spiders/
│ ├── mon_spider.py
│ └── ...
├── pipelines.py
├── app.py
├── Dockerfile.scrapy
├── Dockerfile.flask
├── docker-compose.yml
└── requirements.txt


## Installation et Lancement

### Prérequis

- Docker
- Docker Compose

### Instructions

1. **Cloner le dépôt Git :**
`git clone https://votre-depot.git`
`cd ProjetDataEng`

2. **Lancer l'application :**
Utilisez Docker Compose pour construire et démarrer les services.

`docker-compose up --build`

3. **Accéder à l'application :**
Ouvrez votre navigateur et allez à `http://localhost:8080` pour voir l'application en action.

## Architecture

Décrivez ici l'architecture de votre application, y compris comment les différentes parties (extraction des données, base de données, backend, frontend) interagissent entre elles.

## Contribution

Expliquez comment les autres développeurs peuvent contribuer à votre projet. Incluez les directives pour les contributions, les tests et les pull requests.

## Licence

Indiquez la licence sous laquelle votre projet est distribué.

