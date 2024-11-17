# import logging
# from twisted.internet import reactor, defer
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
# from scrapy.utils.project import get_project_settings

# from web_scraper.spiders.ebay_scraper import EbaySpider
# from web_scraper.spiders.indiamart_scraper import IndiamartSpider

# configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
# runner = CrawlerRunner(get_project_settings())

# print("Starting crawl...")
# @defer.inlineCallbacks
# def crawl():
#     print("Running IndiaMartSpider...")
#     yield runner.crawl(IndiamartSpider)
#     print("Running EbaySpider...")
#     yield runner.crawl(EbaySpider)
#     print("Stopping reactor...")
#     reactor.stop()

# crawl()
# reactor.run()
# print("Script finished.")


from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor, defer
# from ebay_scraper import EbaySpider  # Import your first spider
# from indiamart_scraper import IndiamartSpider  # Import your second spider
from web_scraper.spiders.ebay_scraper import EbaySpider
from web_scraper.spiders.indiamart_scraper import IndiamartSpider
# Define a function to run spiders sequentially
@defer.inlineCallbacks
def run_spiders():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'FEED_FORMAT': 'json',
        # Use different files for each spider's output
        'FEED_URI': 'ebay_products.json',
    })
    
    # Run the first spider
    yield process.crawl(EbaySpider)
    
    # Change the output file for the second spider
    process.settings.set('FEED_URI', 'indiamart_products.json', priority='cmdline')
    
    # Run the second spider
    yield process.crawl(IndiamartSpider)
    
    # Stop the reactor after all spiders are done
    reactor.stop()

# Start the process
run_spiders()
reactor.run()  # The script will block here until all spiders finish
