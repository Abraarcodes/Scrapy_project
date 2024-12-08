import logging
import multiprocessing
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from web_scraper.spiders.indiamart_scraper import IndiamartSpider
from web_scraper.spiders.tradeindia_scraper import TradeIndiaSpider
from web_scraper.spiders.flipkart_spider import FlipkartSpider
from web_scraper.spiders.industrybuying_spider import IndustrybuyingSpider

RESULT_FILES = {
    'IndiamartSpider': 'results/indiamart_products.json',
    'TradeIndiaSpider': 'results/tradeindia_products.json',
    'FlipkartSpider': 'results/flipkart_products.json',
    'IndustrybuyingSpider': 'results/industrybuying_products.json',
}

def run_spider(spider_class, output_file, search_term):
    logging.info(f"Running {spider_class.__name__} for search term: {search_term}")
    settings = get_project_settings()
    settings.set('FEED_FORMAT', 'jsonlines')
    settings.set('FEED_URI', output_file)
    process = CrawlerProcess(settings)
    process.crawl(spider_class, search=search_term)
    process.start()

def run_crawlers_async(search_term):
    processes = []
    spiders = [
        (IndiamartSpider, RESULT_FILES['IndiamartSpider']),
        (TradeIndiaSpider, RESULT_FILES['TradeIndiaSpider']),
        (FlipkartSpider, RESULT_FILES['FlipkartSpider']),
        (IndustrybuyingSpider, RESULT_FILES['IndustrybuyingSpider']),
    ]

    for spider, output_file in spiders:
        p = multiprocessing.Process(target=run_spider, args=(spider, output_file, search_term))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
