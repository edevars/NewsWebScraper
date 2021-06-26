from scrapy.crawler import CrawlerProcess
from spiders.news_eluniversal_spider import ElUniversalSpider
from spiders.news_milenio_spider import MilenioSpider
from spiders.news_unotv_spider import UnoTvSpider
from spiders.news_noticieros_televisa_spider import TelevisaNewsSpider

process = CrawlerProcess()
process.crawl(ElUniversalSpider)
process.crawl(MilenioSpider)
process.crawl(UnoTvSpider)
process.crawl(TelevisaNewsSpider)
process.start()
