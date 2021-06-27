from scrapy.crawler import CrawlerProcess
from spiders.news_eluniversal_spider import ElUniversalSpider
from spiders.news_milenio_spider import MilenioSpider
from spiders.news_unotv_spider import UnoTvSpider
from spiders.news_noticieros_televisa_spider import TelevisaNewsSpider
from utils.get_args import get_args

args = get_args()

try: 
    process = CrawlerProcess()
    process.crawl(ElUniversalSpider, pages=args['--pages-el-universal'])
    process.crawl(MilenioSpider)
    process.crawl(UnoTvSpider)
    process.crawl(TelevisaNewsSpider)
    process.start()
except(KeyError):
    print("\nPlease type the number of pages that you want to scrape")
    print("\nAvailable options: ")
    print("\t--pages-el-universal")