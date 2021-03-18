import scrapy

class NewsSpider(scrapy.Spider):
    name = 'news'
    start_urls = [
        'https://www.excelsior.com.mx/politica'
    ]

    def parse(self, response):
        with open('results.html','w', encoding='UTF-8') as f:
            f.write(response.text)

import scrapy