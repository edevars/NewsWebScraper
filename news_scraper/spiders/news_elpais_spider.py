import scrapy

NAME = 'Milenio'
BASE_URL = 'https://elpais.com/'
TARGET_URL = 'https://elpais.com/mexico/actualidad/'
ARTICLE_LINK = '//h2/a/@href'


class ElPaisSpider(scrapy.Spider):
    name = 'news_elpais'
    start_urls = [TARGET_URL]

    custom_settings = {
        'FEED_URI': './extracted_data/el_pais.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'LOG_STDOUT': True,
        'LOG_FILE': './logs/el_pais.txt',
        'LOG_LEVEL': 'INFO'
    }

    def parse(self, response):
        base_links = response.xpath(ARTICLE_LINK).getall()
        articles_links = [BASE_URL + link for link in base_links]
        for link in articles_links:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': link})

    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        title = response.xpath('//h1/text()').get()
        subtitle = response.xpath('//h2[contains(@class,"a_st")]/text()').get()
        authors = response.xpath('//a[contains(@class,"a_aut_n")]/text()').getall()
        authors = str(authors).replace('[','').replace(']','')
        location = response.xpath('//span[contains(@class,"a_pl")]/text()').get()
        datetime = response.xpath('//a[@class="a_ti"]/text()').get()
        article_paragraphs = response.xpath('//div[@id="ctn_article_body"]/p/descendant-or-self::text()').getall()
        article_text = ''.join(article_paragraphs)

        yield {
            'url': link,
            'title': title,
            'subtitle': subtitle,
            'authors': authors,
            'location': location,
            'date_time': datetime,
            'article_text': article_text
        }
