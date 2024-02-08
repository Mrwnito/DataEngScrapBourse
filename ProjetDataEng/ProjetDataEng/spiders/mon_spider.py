import scrapy

#from elasticsearch import Elasticsearch

class MonSpiderSpider(scrapy.Spider):
    name = "mon_spider"
    indices = {
        'cac_40': '1rPCAC',
        'sbf_120': '1rPPX4',
        'cac_40_esg': '1rPCESGP',
        'ent_pea_pme_150': '1rPENPME'
    }
    
    def start_requests(self):
        for index_name, index_code in self.indices.items():
            url = f'https://www.boursorama.com/cours/{index_code}/_toutes-les-transactions?limit=2000'
            yield scrapy.Request(url, self.parse, cb_kwargs={'index_name': index_name})

    def parse(self, response, index_name):
        table = response.css('body > div > div > div > div > div.c-block__body > table') # Ignorer la première ligne d'en-tête
        table = table[0]
        rows = table.css('tbody > tr.c-table__row')
        for row in rows:
            time = row.css('td:nth-child(1)::text').get()
            price = row.css('td:nth-child(2)::text').get()
            
            if time and price:
                time = time.strip()
                price = price.strip()
                data = {
                    'time': time,
                    'price': price,
                    'index': index_name
                }
                
                yield data

