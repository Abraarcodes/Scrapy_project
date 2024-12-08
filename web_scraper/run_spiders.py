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
cors = CORS(app, resources={r'/scrape': {"origins": CORS_ALLOWED_ORIGINS},r'/save-purchase': {"origins": CORS_ALLOWED_ORIGINS}})

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
    ensures that titles contain all keywords from the search term.
    Saves the filtered data into a single JSON file.
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
                            price_str = data.get('price', '')

                            # Debug: Log the title being checked
                            app.logger.info(f"Checking title: {title}")

                            # Filter out entries with missing title or price
                            if data.get('title') and data.get('price'):
                                # Normalize price string to float (assuming price is in ₹)
                                price = normalize_price(price_str)

                                # Debug: Check and log the price
                                app.logger.info(f"Normalized price: {price}")

                                # Filter based on search keywords in the title
                                if all(re.search(r'\b' + re.escape(keyword) + r'\b', title) for keyword in search_keywords):
                                    # Append the data to the combined list
                                    combined_data.append(data)
                                else:
                                    app.logger.info(f"Title does not match all keywords: {title}")
                            else:
                                app.logger.info(f"Skipping due to missing title or price: {data}")
                        except json.JSONDecodeError as e:
                            app.logger.error(f"Error decoding line in {file_name}: {e}")
            except Exception as e:
                app.logger.error(f"Error reading {file_name}: {e}")

    # Benchmarking - sort by price (low to high)
    combined_data.sort(key=lambda x: normalize_price(x['price']))

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


def normalize_price(price_str):
    """
    Normalizes the price string into a numerical format.
    Assumes the price string contains a currency symbol and removes non-numeric characters.
    """
    # Remove currency symbols and commas (e.g., ₹, $, ,) and convert the price to float
    price_str = re.sub(r'[^\d.]', '', price_str)
    
    try:
        return float(price_str)
    except ValueError:
        return 0.0  # In case of invalid price format, return 0


def calculate_average_price(data):
    """
    Calculates the average price from the combined data.
    This function is no longer needed since there's no benchmark price to compare.
    """
    total_price = sum(normalize_price(item['price']) for item in data)
    count = len(data)
    return total_price / count if count > 0 else 0.0  # Return 0.0 if no valid data


PURCHASES_FILE = 'purchases.json'

@app.route('/save-purchase', methods=['POST'])
def save_purchase():
    """
    Flask route to save purchase data sent from the frontend.
    It appends the new purchase data to the purchases.json file.
    """
    try:
        # Get the JSON data from the POST request
        data = request.get_json()
        
        # Extract product details
        title = data.get('title')
        price = data.get('price')
        link = data.get('link')
        
        # Check if all fields are present
        if not title or not price or not link:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400

        # Prepare the product data
        purchase_data = {
            'title': title,
            'price': price,
            'link': link,
        }

        # Check if the purchases.json file exists, if not, create it
        if os.path.exists(PURCHASES_FILE):
            with open(PURCHASES_FILE, 'r') as file:
                existing_purchases = json.load(file)
        else:
            existing_purchases = []

        # Append the new purchase to the existing list
        existing_purchases.append(purchase_data)

        # Save the updated data back to the JSON file
        with open(PURCHASES_FILE, 'w') as file:
            json.dump(existing_purchases, file, indent=4)

        return jsonify({'success': True})

    except Exception as e:
        app.logger.error(f"Error saving purchase: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

if __name__ == '__main__':
    benchmark_price = None
    app.run(debug=True)
