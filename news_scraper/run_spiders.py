from scrapy.crawler import CrawlerProcess
from spiders.news_eluniversal_spider import ElUniversalSpider
from spiders.news_milenio_spider import MilenioSpider

process = CrawlerProcess()
process.crawl(ElUniversalSpider)
process.crawl(MilenioSpider)
process.start()