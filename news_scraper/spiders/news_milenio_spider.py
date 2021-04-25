import scrapy

NAME = 'Milenio'
BASE_URL = 'https://www.milenio.com'
TARGET_URL = 'https://www.milenio.com/politica'
ARTICLE_LINK = '//div[@class="title"]/a/@href'


class MilenioSpider(scrapy.Spider):
    name = 'news_milenio'
    start_urls = [TARGET_URL]

    custom_settings = {
        'FEED_URI': './extracted_data/milenio.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'LOG_STDOUT': True,
        'LOG_FILE': '/tmp/scrapy_eluniversal.txt',
        'LOG_LEVEL': 'INFO'
    }

    def parse(self, response):
        base_links = response.xpath(ARTICLE_LINK).getall()
        articles_links = [BASE_URL + link for link in base_links]
        for link in articles_links:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': link})

    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        title = response.xpath('//h1[@class="title"]/text()').get()
        author = response.xpath(
            '//div[@class="nd-content-body"]/span[@class="author"]/text()').get()
        location = response.xpath(
            '//div[@class="content-date"]/span[@class="location"]/text()').get()
        datetime = response.xpath('//time/@datetime').get()
        article_paragraphs = response.xpath(
            '//div[@id="content-body"]/p/descendant-or-self::text()').getall()
        article_text = ''.join(article_paragraphs)

        yield {
            'url': link,
            'title': title,
            'author': author,
            'location': location,
            'date_time': datetime,
            'article_text': article_text
        }
