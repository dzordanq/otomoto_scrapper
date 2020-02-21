from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from otomoto.spiders.otomoto_spider import OtomotoSpider


settings = get_project_settings()
process = CrawlerProcess(settings=settings)

process.crawl(OtomotoSpider)
process.start()
