import scrapy

NAME = 'Uno TV'
BASE_URL = 'https://www.unotv.com'
TARGET_URL = 'https://www.unotv.com/nacional'
ARTICLE_LINK = '//h2[@class="entry-title"]/a/@href'


class UnoTvSpider(scrapy.Spider):
    name = 'news_unotv'
    start_urls = [TARGET_URL]

    custom_settings = {
        'FEED_URI': './extracted_data/unotv.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'LOG_STDOUT': True,
        'LOG_FILE': '/tmp/scrapy_unotv.txt',
        'LOG_LEVEL': 'INFO'
    }

    def parse(self, response):
        article_links = response.xpath(ARTICLE_LINK).getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': link})

    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        title = response.xpath('//h1[@class="entry-title"]/text()').get()
        'location regex: \|.+\|'
        header_info = response.xpath(
            '//span[@class="byline"]/text()').get()
        header_info = header_info.split('|')

        author = header_info[0]
        location = header_info[1]
        datetime = response.xpath('//time/@datetime').get()
        article_paragraphs = response.xpath(
            '//div[@class="entry-content"]/p/descendant-or-self::text()').getall()
        
        article_text = ''.join(article_paragraphs)

        yield {
            'url': link,
            'title': title,
            'author': author,
            'location': location,
            'date_time': datetime,
            'article_text': article_text
        }
