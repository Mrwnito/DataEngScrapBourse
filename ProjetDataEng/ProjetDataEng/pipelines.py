from pymongo import MongoClient
from itemadapter import ItemAdapter
# from elasticsearch import Elasticsearch
import os
import re

class ProjetdataengPipeline:
    """
    Pipeline pour traiter et stocker les éléments scrapés dans MongoDB.
    
    Méthodes :
        open_spider(self, spider) : Initialise la connexion à MongoDB à l'ouverture du spider.
        close_spider(self, spider) : Ferme la connexion à MongoDB à la fermeture du spider.
        process_item(self, item, spider) : Traite chaque élément scrapé et l'enregistre dans MongoDB.
        get_latest_data(index_name) : Récupère les dernières données d'un indice spécifique depuis MongoDB.
        calculate_percentage_change(clean_data) : Calcule le pourcentage de changement des prix.
    """
    
    def open_spider(self, spider):
        """
        Initialisation de la connexion à MongoDB et Elasticsearch (si nécessaire) à l'ouverture du spider.
        """
        mongo_host = os.getenv('MONGO_HOST', 'localhost')
        self.client = MongoClient(f'mongodb://{mongo_host}:27017/')
        self.db = self.client['DATA_db']

        # Initialisation d'une connexion à Elasticsearch
        # self.es = Elasticsearch(['http://localhost:9200'])

    def close_spider(self, spider):
        """
        Ferme la connexion à MongoDB à la fermeture du spider.
        """
        self.client.close()

    def process_item(self, item, spider):
        """
        Traite chaque élément scrapé, le convertit en utilisant ItemAdapter et l'enregistre dans MongoDB.
        """
        adapter = ItemAdapter(item)
        index_name = adapter['index']
        document_id = f"{adapter['time']}-{adapter['price']}"

        # Préparation du document pour MongoDB et tentative d'insertion ou de mise à jour
        self.db[adapter['index']].update_one(
            {"time": adapter['time'], "price": adapter['price']},
            {"$setOnInsert": {"time": adapter['time'], "price": adapter['price']}},
            upsert=True
        )

        # Code pour l'envoi à Elasticsearch (commenté car non utilisé)
        # self.es.update(
        #    index=index_name, 
        #    id=document_id, 
        #    body={"doc": {"time": adapter['time'], "price": adapter['price']}, "doc_as_upsert": True}
        # )
        
        return item

    @staticmethod
    def get_latest_data(index_name):
        """
        Récupère les dernières données pour un indice spécifique depuis MongoDB et nettoie les prix.
        """
        mongo_host = os.getenv('MONGO_HOST', 'localhost')
        client = MongoClient(f'mongodb://{mongo_host}:27017/')
        db = client['DATA_db']
        collection = db[index_name]
        data = list(collection.find().sort([("time", 1)]).limit(2000))

        # Nettoyage des prix dans les données récupérées
        for entry in data:
            entry['price'] = float(re.sub(r'[^\d.]', '', entry['price']))

        client.close()
        return data

    @staticmethod
    def calculate_percentage_change(clean_data):
        """
        Calcule le pourcentage de changement par rapport au premier élément de la liste.
        """
        if not clean_data:
            return []
        
        reference_value = clean_data[0]['price']
        percentage_changes = [round((point['price'] - reference_value) / reference_value * 100, 2) for point in clean_data]
        return percentage_changes

    
