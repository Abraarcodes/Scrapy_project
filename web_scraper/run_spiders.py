import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from web_scraper.spiders.indiamart_scraper import IndiamartSpider
import os
import json

app = Flask(__name__)
CORS(app)
# Set up logging for Flask
logging.basicConfig(level=logging.DEBUG)

@app.route('/scrape', methods=['GET'])
def scrape():
    search_term = request.args.get('search', '')
    
    if not search_term:
        return jsonify({'error': 'No search term provided'}), 400

    app.logger.info(f"Starting scrape for search term: {search_term}")
    
    # Set up the Scrapy process
    process = CrawlerProcess(get_project_settings())
    process.crawl(IndiamartSpider, search=search_term)
    
    # Start the Scrapy crawler and wait for it to finish
    app.logger.info("Starting the Scrapy process...")
    process.start()
    
    # After scraping, check if the JSON result file exists
    result_file = 'indiamart_products.json'
    app.logger.info(f"Checking for result file: {result_file}")
    
    if os.path.exists(result_file):
        with open(result_file, 'r') as f:
            data = json.load(f)
        app.logger.info(f"Scraping complete. Found {len(data)} products.")
        return jsonify(data)
    
    app.logger.error('Failed to scrape or no results found.')
    return jsonify({'error': 'Failed to scrape or no results found'}), 500

if __name__ == '__main__':
    app.run(debug=True)
