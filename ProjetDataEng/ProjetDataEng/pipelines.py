from pymongo import MongoClient
from itemadapter import ItemAdapter
#from elasticsearch import Elasticsearch
import os
import re

class ProjetdataengPipeline:
    def open_spider(self, spider):
        mongo_host = os.getenv('MONGO_HOST', 'localhost')
        self.client = MongoClient(f'mongodb://{mongo_host}:27017/')
        self.db = self.client['DATA_db']

        #self.es = Elasticsearch(['http://localhost:9200'])  # Assure-toi que cette URL est correcte

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        index_name = adapter['index']

        # Construisez un identifiant unique pour le document, par exemple, en combinant le temps et le prix
        document_id = f"{adapter['time']}-{adapter['price']}"

        # Préparez le document pour l'indexation
        document_body = {"time": adapter['time'], "price": adapter['price']}
        # Enregistrement dans MongoDB
        self.db[adapter['index']].update_one(
            {"time": adapter['time'], "price": adapter['price']},
            {"$setOnInsert": {"time": adapter['time'], "price": adapter['price']}},
            upsert=True
        )
        
        # Envoi à Elasticsearch
        # Indexez le document dans Elasticsearch avec upsert
        #self.es.update(
         #   index=index_name, 
         #   id=document_id, 
          #  body={"doc": document_body, "doc_as_upsert": True}
        #)
        
        return item
    
    @staticmethod
    def get_latest_data(index_name):
        mongo_host = os.getenv('MONGO_HOST', 'localhost')
        client = MongoClient(f'mongodb://{mongo_host}:27017/')
        db = client['DATA_db']
        collection = db[index_name]
        data = list(collection.find().sort([("time", 1)]).limit(2000))

        # Convertir chaque élément de la liste 'data' séparément
        for entry in data:
            entry['price'] = float(re.sub(r'[^\d.]', '', entry['price']))

        client.close()
        return data
    
    @staticmethod
    def calculate_percentage_change(clean_data):
        if not clean_data:  # Vérifie que clean_data n'est pas vide
            return []
            
        reference_value = clean_data[0]['price'] # Le premier prix de la liste est pris comme référence
        percentage_changes = []
        for point in clean_data:
            change = (point['price'] - reference_value) / reference_value * 100
            percentage_changes.append(round(change, 2))  # Arrondir à deux décimales
        return percentage_changes
    