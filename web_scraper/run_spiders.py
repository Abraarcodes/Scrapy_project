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
import re

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
    Flask route to initiate the scraping process and return combined, filtered results.
    """
    search_term = request.args.get('search', '')
    app.logger.info(f"Received search term: {search_term}")
    if not search_term:
        return jsonify({'error': 'No search term provided'}), 400

    app.logger.info(f"Starting scraping for search term: {search_term}")

    # Delete existing result files
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
    combined_results = []
    timeout = 60  # Maximum time to wait in seconds
    interval = 5  # Time to wait between subsequent checks
    waited_time = 10  # Account for the initial delay

    while waited_time < timeout:
        all_files_ready = True
        for spider_name, file_name in RESULT_FILES.items():
            file_path = os.path.join(os.getcwd(), file_name)  # Ensure the path is valid
            if not os.path.exists(file_path):
                all_files_ready = False
                app.logger.info(f"Waiting for {file_name} to be created...")
                break

        if all_files_ready:
            break  # Exit loop if all files are ready
        else:
            time.sleep(interval)
            waited_time += interval

    # If timeout occurs, include a warning in the response
    if waited_time >= timeout:
        app.logger.warning("Timeout occurred before all results were available.")

    # Combine and filter the results
    combined_results = combine_and_filter_results(search_term=search_term)

    return jsonify(combined_results)


def combine_and_filter_results(output_file='products.json', search_term=''):
    """
    Combines data from individual spider result files, filters out entries with missing titles or prices,
    and ensures that titles contain all keywords from the search term. Saves the filtered data into a single JSON file.
    """
    combined_data = []

    # Debug: Log the search term
    app.logger.info(f"Raw search term: {search_term}")

    # Split the search term into individual keywords and remove any extra spaces
    search_keywords = [keyword.strip().lower() for keyword in search_term.split('+')]

    # Debug: Log the processed search keywords
    app.logger.info(f"Processed search keywords: {search_keywords}")

    for spider_name, file_name in RESULT_FILES.items():
        file_path = os.path.join(os.getcwd(), file_name)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    for line in f:
                        try:
                            # Load each JSON object
                            data = json.loads(line.strip())
                            title = data.get('title', '').lower()

                            # Debug: Log the title being checked
                            app.logger.info(f"Checking title: {title}")

                            # Filter out entries with missing title or price
                            if data.get('title') and data.get('price'):
                                # Debug: Check and log keyword matching
                                matching_keywords = []
                                for kw in search_keywords:
                                    match = re.search(r'\b' + re.escape(kw) + r'\b', title)
                                    if match:
                                        matching_keywords.append(kw)

                                app.logger.info(f"Matching keywords in title: {matching_keywords}")

                                # Check if all search keywords are in the title (as whole words)
                                if all(re.search(r'\b' + re.escape(keyword) + r'\b', title) for keyword in search_keywords):
                                    app.logger.info(f"Title matches all keywords: {title}")
                                    combined_data.append(data)
                                else:
                                    app.logger.info(f"Title does not match all keywords: {title}")
                            else:
                                app.logger.info(f"Skipping due to missing title or price: {data}")
                        except json.JSONDecodeError as e:
                            app.logger.error(f"Error decoding line in {file_name}: {e}")
            except Exception as e:
                app.logger.error(f"Error reading {file_name}: {e}")

    # Save the combined and filtered data to the output file
    try:
        with open(output_file, 'w') as output:
            json.dump(combined_data, output, indent=4)
            app.logger.info(f"Filtered data written to {output_file}")
    except Exception as e:
        app.logger.error(f"Error writing to {output_file}: {e}")

    # Debug: Log the final filtered results
    app.logger.info(f"Final filtered data: {combined_data}")

    return combined_data




if __name__ == '__main__':
    app.run(debug=True)
