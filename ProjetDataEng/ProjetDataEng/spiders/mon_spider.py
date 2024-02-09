import scrapy

# from elasticsearch import Elasticsearch

class MonSpiderSpider(scrapy.Spider):
    """
    Spider pour scraper les données des transactions des indices boursiers sur Boursorama.

    Attributs :
        name (str): Nom unique du spider.
        indices (dict): Dictionnaire des indices boursiers et leurs codes correspondants sur Boursorama.
    """
    
    name = "mon_spider"
    indices = {
        'cac_40': '1rPCAC',
        'sbf_120': '1rPPX4',
        'cac_40_esg': '1rPCESGP',
        'ent_pea_pme_150': '1rPENPME'
    }
    
    def start_requests(self):
        """
        Méthode pour générer les requêtes initiales pour chaque indice boursier.

        Yields :
            scrapy.Request: Requête Scrapy pour scraper les données de transactions pour chaque indice.
        """
        for index_name, index_code in self.indices.items():
            url = f'https://www.boursorama.com/cours/{index_code}/_toutes-les-transactions?limit=2000'
            yield scrapy.Request(url, self.parse, cb_kwargs={'index_name': index_name})

    def parse(self, response, index_name):
        """
        Callback pour traiter la réponse de chaque requête générée par start_requests.

        Paramètres :
            response (scrapy.http.Response): Réponse à la requête.
            index_name (str): Nom de l'indice boursier correspondant à la réponse.

        Yields :
            dict: Dictionnaire contenant l'heure, le prix et l'indice de chaque transaction.
        """
        # Sélection de la table contenant les données des transactions.
        table = response.css('body > div > div > div > div > div.c-block__body > table')[0]
        rows = table.css('tbody > tr.c-table__row')
        
        for row in rows:
            # Extraction de l'heure et du prix pour chaque transaction.
            time = row.css('td:nth-child(1)::text').get()
            price = row.css('td:nth-child(2)::text').get()
            
            # Nettoyage et structuration des données extraites.
            if time and price:
                time = time.strip()
                price = price.strip()
                data = {
                    'time': time,
                    'price': price,
                    'index': index_name
                }
                
                yield data
