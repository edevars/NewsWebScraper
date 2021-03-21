import scrapy

NAME= 'Milenio'
BASE_URL = 'https://www.milenio.com'
TARGET_URL = 'https://www.milenio.com/politica'
ARTICLE_LINK = '//div[@class="title"]/a/@href'

class NewsSpider(scrapy.Spider):
    name = 'news_milenio'
    start_urls = [TARGET_URL]

    def parse(self, response):
        print("*" * 10)
        print("\n" * 3)
        articles = response.xpath(ARTICLE_LINK).getall()
        for article in articles:
            print(BASE_URL + article)
        print("\n" * 3)
        print("*" * 10)
