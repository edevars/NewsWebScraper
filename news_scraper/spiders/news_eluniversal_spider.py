import scrapy

NAME = 'El Universal'
BASE_URL = 'https://www.milenio.com'
TARGET_URL = 'https://activo.eluniversal.com.mx/historico/search/indexCesar.php?q=politica&anio=&seccion=&opinion=&tipo_contenido=&autor=&tipoedicion=&dia=&mes=&rango_Fechas=&k_rango_fechas=&fecha_ini=&fecha_fin=&editor=&start=20&page=2'
ARTICLE_LINK = '//div[@class="moduloNoticia"]//div[@class="FechaSeccion"]/span[@class="Seccion"]/text()[contains(.,"Estados") or contains(.,"Nación") or contains(.,"Metrópoli")]/ancestor::div[2]//a/@href'


class NewsSpider(scrapy.Spider):
    name = 'news_eluniversal'
    start_urls = [TARGET_URL]

    custom_settings = {
        'FEED_URI': 'eluniversal.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        articles_links = response.xpath(ARTICLE_LINK).getall()
        for link in articles_links:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': link})

    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        section = response.xpath(
            '//a[@class="ce12-DatosArticulo_TiempoRelojes"]/text()').get()
        title = response.xpath('//h1/text()').get()
        subtitle = response.xpath('//h2/text()').get()
        author = response.xpath(
            '//span[@class="ce12-DatosArticulo_autor"]/text()').get()
        location = response.xpath(
            '//div[@class="content-date"]/span[@class="location"]/text()').get()
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
            'location': location,
            'date_time': datetime,
            'article_text': article_text
        }
