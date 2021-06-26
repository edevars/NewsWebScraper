import scrapy

NAME = 'televisa.NEWS'
ARTICLE_LINK = '//h4[@class="tile_ni_heading"]/a/@href'


def generate_urls(n):
    urls = []
    for i in range(n):
        url = f'https://noticieros.televisa.com/topico/politica/page/{n}/'
        urls.append(url)
    return urls


class TelevisaNewsSpider(scrapy.Spider):
    name = 'news_televisa'
    start_urls = generate_urls(1)

    custom_settings = {
        'FEED_URI': './extracted_data/televisa_news.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'LOG_STDOUT': True,
        'LOG_FILE': '/tmp/scrapy_televisa.txt',
        'LOG_LEVEL': 'INFO'
    }

    def parse(self, response):
        articles_links = response.xpath(ARTICLE_LINK).getall()

        for link in articles_links:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': link})

    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        topic = response.xpath(
            '//span[@class="topico_container"]/a/@title').get()
        title = response.xpath('//h1[@class="article_title"]/text()').get()
        subtitle = response.xpath(
            '//div[@class="article_heading"]/p/text()').get()
        author = response.xpath(
            '//span[@class="article_author"]/a/text()').get()
        datetime = response.xpath(
            '//time[@class="post_datetime"]/@datetime').get()
        article_paragraphs = article_paragraphs = response.xpath(
            '//div[@class="post_content inner_wrapper"]/*[self::p or self::blockquote]/descendant-or-self::text()').getall()
        article_text = ''.join(article_paragraphs)

        yield {
            'url': link,
            'title': title,
            'subtitle': subtitle,
            'topic': topic,
            'author': author,
            'date_time': datetime,
            'article_text': article_text
        }
