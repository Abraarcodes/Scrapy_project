import time
import logging
import multiprocessing  # Import multiprocessing
from flask import Flask, request, jsonify
from flask_cors import CORS
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from web_scraper.spiders.indiamart_scraper import IndiamartSpider
from web_scraper.spiders.tradeindia_scraper import TradeIndiaSpider
from web_scraper.spiders.flipkart_spider import FlipkartSpider
from web_scraper.spiders.industrybuying_spider import IndustrybuyingSpider
import os
import json

app = Flask(__name__)

CORS_ALLOWED_ORIGINS = ['http://localhost:5173']  # Replace with your frontend origin
cors = CORS(app, resources={r'/scrape': {"origins": CORS_ALLOWED_ORIGINS}})

# Set up logging for Flask
logging.basicConfig(level=logging.DEBUG)

# Store result file names for each spider
RESULT_FILES = {
    'IndiamartSpider': 'indiamart_products.json',
    'TradeIndiaSpider': 'tradeindia_products.json',
    'FlipkartSpider':'flipkart_products.json',
    'IndustrybuyingSpider':'industrybuying_products.json',
}

def run_indiamart_spider(search_term):
    logging.info(f"Running IndiamartSpider for search term: {search_term}")
    settings = get_project_settings()
    settings.set('FEED_FORMAT', 'jsonlines')  # Ensure correct format
    settings.set('FEED_URI', 'indiamart_products.json')
    process = CrawlerProcess(settings)
    process.crawl(IndiamartSpider, search=search_term)
    process.start()

def run_tradeindia_spider(search_term):
    logging.info(f"Running TradeIndiaSpider for search term: {search_term}")
    settings = get_project_settings()
    settings.set('FEED_FORMAT', 'jsonlines')  # Ensure correct format
    settings.set('FEED_URI', 'tradeindia_products.json')
    process = CrawlerProcess(settings)
    process.crawl(TradeIndiaSpider, search=search_term)
    process.start()

def run_flipkart_spider(search_term):
    logging.info(f"Running FlipkartSpider for search term: {search_term}")
    settings = get_project_settings()
    settings.set('FEED_FORMAT', 'jsonlines')  # Ensure correct format
    settings.set('FEED_URI', 'flipkart_products.json')
    process = CrawlerProcess(settings)
    process.crawl(FlipkartSpider, search=search_term)
    process.start()

def run_industrybuying_spider(search_term):
    logging.info(f"Running IndustryBuyingSpider for search term: {search_term}")
    settings = get_project_settings()
    settings.set('FEED_FORMAT', 'jsonlines')  # Ensure correct format
    settings.set('FEED_URI', 'industrybuying_products.json')
    process = CrawlerProcess(settings)
    process.crawl(IndustrybuyingSpider, search=search_term)
    process.start()

def run_crawlers_async(search_term):
    """
    Run spiders concurrently using multiprocessing.
    """
    # Running the spiders concurrently using multiprocessing
    indiamart_process = multiprocessing.Process(target=run_indiamart_spider, args=(search_term,))
    tradeindia_process = multiprocessing.Process(target=run_tradeindia_spider, args=(search_term,))
    flipkart_process=multiprocessing.Process(target=run_flipkart_spider, args=(search_term,))
    industrybuyingSpider_process=multiprocessing.Process(target=run_industrybuying_spider, args=(search_term,))

    indiamart_process.start()
    tradeindia_process.start()
    flipkart_process.start()
    industrybuyingSpider_process.start()

    indiamart_process.join()
    tradeindia_process.join()
    flipkart_process.join()
    industrybuyingSpider_process.join()


@app.route('/scrape', methods=['GET'])
def scrape():
    """
    Flask route to initiate the scraping process.
    """
    search_term = request.args.get('search', '')
    print("Search term",search_term)
    if not search_term:
        return jsonify({'error': 'No search term provided'}), 400

    app.logger.info(f"Starting scraping for search term: {search_term}")

    products_file_path = os.path.join(os.getcwd(), 'products.json')
    if os.path.exists(products_file_path):
        try:
            os.remove(products_file_path)
            app.logger.info(f"Deleted existing file: products.json")
        except Exception as e:
            app.logger.error(f"Error deleting products.json: {e}")

    for spider_name, file_name in RESULT_FILES.items():
        file_path = os.path.join(os.getcwd(), file_name)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                app.logger.info(f"Deleted existing file: {file_name}")
            except Exception as e:
                app.logger.error(f"Error deleting {file_name}: {e}")
    # Run the scraping process using multiprocessing
    run_crawlers_async(search_term)

    # Wait for scraping to complete and collect results
    combined_results = {}
    timeout = 60  # Maximum time to wait in seconds
    interval = 5  # Time to wait between subsequent checks
    waited_time = 10  # Account for the initial delay

    while waited_time < timeout:
        all_files_ready = True
        for spider_name, file_name in RESULT_FILES.items():
            file_path = os.path.join(os.getcwd(), file_name)  # Ensure the path is valid
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        combined_results[spider_name] = []
                        for line in f:
                            try:
                                # Load each JSON object from the file
                                data = json.loads(line.strip())
                                combined_results[spider_name].append(data)
                            except json.JSONDecodeError as e:
                                app.logger.error(f"Error decoding line in {file_name}: {e}")
                except Exception as e:
                    app.logger.error(f"Error reading {file_name}: {e}")
            else:
                all_files_ready = False
                app.logger.info(f"Waiting for {file_name} to be created...")

        if all_files_ready:
            break  # Exit loop if all files are ready
        else:
            time.sleep(interval)
            waited_time += interval

    # If timeout occurs, include a warning in the response
    if waited_time >= timeout:
        for spider_name, file_name in RESULT_FILES.items():
            if spider_name not in combined_results:
                combined_results[spider_name] = []
        app.logger.warning("Timeout occurred before all results were available.")

    return jsonify(combined_results)


if __name__ == '__main__':
    app.run(debug=True)
