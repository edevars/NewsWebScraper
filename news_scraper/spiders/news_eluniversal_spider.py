import scrapy

NAME = 'El Universal'
BASE_URL = 'https://www.milenio.com'
TARGET_URL = 'https://activo.eluniversal.com.mx/historico/search/indexCesar.php?q=politica&anio=&seccion=&opinion=&tipo_contenido=&autor=&tipoedicion=&dia=&mes=&rango_Fechas=&k_rango_fechas=&fecha_ini=&fecha_fin=&editor=&start=20&page=2'
ARTICLE_LINK = '//div[@class="moduloNoticia"]//div[@class="FechaSeccion"]/span[@class="Seccion"]/text()[contains(.,"Estados") or contains(.,"Nación") or contains(.,"Metrópoli")]/ancestor::div[2]//a/@href'


def generate_urls(n):
    urls = []
    for i in range(n):
        url = f'https://activo.eluniversal.com.mx/historico/search/indexCesar.php?q=politica&anio=&seccion=&opinion=&tipo_contenido=&autor=&tipoedicion=&dia=&mes=&rango_Fechas=&k_rango_fechas=&fecha_ini=&fecha_fin=&editor=&start={i*20}&page={i+1}'
        urls.append(url)
    return urls

def clean_opinion_links(links):
    clean_links = []
    for link in links:
        if(link.find('opinion')==-1):
            clean_links.append(link)
    return clean_links

class NewsSpider(scrapy.Spider):
    name = 'news_eluniversal'
    start_urls = generate_urls(1)

    custom_settings = {
        'FEED_URI': './extracted_data/el_universal.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'LOG_STDOUT': True,
        'LOG_FILE': '/tmp/scrapy_eluniversal.txt',
        'LOG_LEVEL': 'INFO'
    }

    def parse(self, response):
        articles_links = response.xpath(ARTICLE_LINK).getall()
        # articles that aren't from the opinion section
        clean_links = clean_opinion_links(articles_links)

        for link in clean_links:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': link})

    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        section = response.xpath(
            '//a[@class="ce12-DatosArticulo_TiempoRelojes"]/text()').get()
        title = response.xpath('//*[contains(@class,"h1")]/text()').get()
        subtitle = response.xpath('//h2[@class="h2"]/text()').get()
        author = response.xpath(
            '//span[@class="ce12-DatosArticulo_autor"]/text()').get()
        datetime = response.xpath(
            '//span[@class="ce12-DatosArticulo_ElementoFecha"]/text()').get()
        article_paragraphs = response.xpath(
            '//div[@class="field field-name-body field-type-text-with-summary field-label-hidden"]/p/descendant-or-self::text()').getall()
        article_text = ''.join(article_paragraphs)

        yield {
            'url': link,
            'title': title,
            'subtitle': subtitle,
            'section': section,
            'author': author,
            'date_time': datetime,
            'article_text': article_text
        }
