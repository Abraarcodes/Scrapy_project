# import logging
# import threading
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# from web_scraper.spiders.indiamart_scraper import IndiamartSpider
# from web_scraper.spiders.tradeindia_scraper import TradeIndiaSpider
# import os
# import json

# app = Flask(__name__)

# CORS_ALLOWED_ORIGINS = ['http://localhost:5173']  # Replace with your frontend origin
# cors = CORS(app, resources={r'/scrape': {"origins": CORS_ALLOWED_ORIGINS}})



# # Set up logging for Flask
# logging.basicConfig(level=logging.DEBUG)

# # Store result file names for each spider
# RESULT_FILES = {
#     'IndiamartSpider': 'indiamart_products.json',
#     'TradeIndiaSpider': 'tradeindia_products.json'
# }


# def run_crawlers(search_term):
#     """
#     Run spiders sequentially in a separate thread.
#     """
#     try:
#         # Get Scrapy project settings
#         settings = get_project_settings()
#         settings.set('FEED_FORMAT', 'json')
#         settings.set('INSTALL_SHUTDOWN_HANDLERS', False)  # Prevent Scrapy from stopping the reactor

#         # Set up the Scrapy process
#         process = CrawlerProcess(settings)

#         # Run IndiamartSpider
#         logging.info(f"Running IndiamartSpider for search term: {search_term}")
#         process.crawl(IndiamartSpider, search=search_term)

#         # Run TradeIndiaSpider after IndiamartSpider
#         # logging.info(f"Running TradeIndiaSpider for search term: {search_term}")
#         # process.crawl(TradeIndiaSpider, search=search_term)

#         # Start the process (blocks until both spiders finish)
#         process.start()
#         logging.info("All spiders finished successfully.")

#     except Exception as e:
#         logging.error(f"Error during scraping: {str(e)}")


# @app.route('/scrape', methods=['GET'])
# def scrape():
#     """
#     Flask route to initiate the scraping process.
#     """
#     search_term = request.args.get('search', '')

#     if not search_term:
#         return jsonify({'error': 'No search term provided'}), 400

#     app.logger.info(f"Starting scraping for search term: {search_term}")

#     # Run the scraping process in a separate thread
#     scraping_thread = threading.Thread(target=run_crawlers, args=(search_term,))
#     scraping_thread.start()

#     # return jsonify({'status': 'Scraping started. Results will be available soon.'})
#     combined_results = {}
#     for spider_name, file_name in RESULT_FILES.items():
#         if os.path.exists(file_name):
#             with open(file_name, 'r') as f:
#                 combined_results[spider_name] = json.load(f)
#             app.logger.info(f"Loaded results for {spider_name}.")
#         else:
#             app.logger.warning(f"No results found for {spider_name}.")
#             combined_results[spider_name] = []


#     return jsonify(combined_results)


# if __name__ == '__main__':
#     app.run(debug=True)













#works above goood 















import time
import logging
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from web_scraper.spiders.indiamart_scraper import IndiamartSpider
from web_scraper.spiders.tradeindia_scraper import TradeIndiaSpider
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
    'TradeIndiaSpider': 'tradeindia_products.json'
}

def run_crawlers(search_term):
    """
    Run spiders sequentially in a separate thread.
    """
    try:
        # Get Scrapy project settings
        settings = get_project_settings()
        settings.set('FEED_FORMAT', 'json')
        settings.set('INSTALL_SHUTDOWN_HANDLERS', False)  # Prevent Scrapy from stopping the reactor

        # Set up the Scrapy process
        process = CrawlerProcess(settings)

        # Run IndiamartSpider
        logging.info(f"Running IndiamartSpider for search term: {search_term}")
        process.crawl(IndiamartSpider, search=search_term)

        # Run TradeIndiaSpider after IndiamartSpider (if needed)
        logging.info(f"Running TradeIndiaSpider for search term: {search_term}")
        process.crawl(TradeIndiaSpider, search=search_term)

        # Start the process (blocks until both spiders finish)
        process.start()
        logging.info("All spiders finished successfully.")

    except Exception as e:
        logging.error(f"Error during scraping: {str(e)}")

# @app.route('/scrape', methods=['GET'])
# def scrape():
#     """
#     Flask route to initiate the scraping process.
#     """
#     search_term = request.args.get('search', '')

#     if not search_term:
#         return jsonify({'error': 'No search term provided'}), 400

#     app.logger.info(f"Starting scraping for search term: {search_term}")

#     # Run the scraping process in a separate thread
#     scraping_thread = threading.Thread(target=run_crawlers, args=(search_term,))
#     scraping_thread.start()

#     # Wait for scraping to complete and collect results
#     combined_results = {}
#     for spider_name, file_name in RESULT_FILES.items():
#         file_path = os.path.join(os.getcwd(), file_name)  # Make sure the path is valid
#         if os.path.exists(file_path):
#             with open(file_path, 'r') as f:
#                 combined_results[spider_name] = json.load(f)
#             app.logger.info(f"Loaded results for {spider_name}.")
#         else:
#             app.logger.warning(f"No results found for {spider_name}.")
#             combined_results[spider_name] = []

#     return jsonify(combined_results)




# @app.route('/scrape', methods=['GET'])
# def scrape():
#     """
#     Flask route to initiate the scraping process.
#     """
#     search_term = request.args.get('search', '')

#     if not search_term:
#         return jsonify({'error': 'No search term provided'}), 400

#     app.logger.info(f"Starting scraping for search term: {search_term}")

#     # Run the scraping process in a separate thread
#     scraping_thread = threading.Thread(target=run_crawlers, args=(search_term,))
#     scraping_thread.start()

#     # Wait for scraping to complete and collect results
#     combined_results = {}
#     timeout = 60  # Maximum time to wait in seconds
#     interval = 5  # Time to wait between checks
#     waited_time = 0

#     while waited_time < timeout:
#         all_files_ready = True
#         for spider_name, file_name in RESULT_FILES.items():
#             file_path = os.path.join(os.getcwd(), file_name)  # Ensure the path is valid
#             if os.path.exists(file_path):
#                 with open(file_path, 'r') as f:
#                     combined_results[spider_name] = json.load(f)
#                 app.logger.info(f"Loaded results for {spider_name}.")
#             else:
#                 all_files_ready = False
#                 app.logger.info(f"Waiting for {file_name} to be created...")

#         if all_files_ready:
#             break  # Exit loop if all files are ready
#         else:
#             time.sleep(interval)
#             waited_time += interval

#     # If timeout occurs, include a warning in the response
#     if waited_time >= timeout:
#         for spider_name, file_name in RESULT_FILES.items():
#             if spider_name not in combined_results:
#                 combined_results[spider_name] = []
#         app.logger.warning("Timeout occurred before all results were available.")

#     return jsonify(combined_results)


# if __name__ == '__main__':
#     app.run(debug=True)



@app.route('/scrape', methods=['GET'])
def scrape():
    """
    Flask route to initiate the scraping process.
    """
    search_term = request.args.get('search', '')

    if not search_term:
        return jsonify({'error': 'No search term provided'}), 400

    app.logger.info(f"Starting scraping for search term: {search_term}")

    # Run the scraping process in a separate thread
    scraping_thread = threading.Thread(target=run_crawlers, args=(search_term,))
    scraping_thread.start()

    # Initial delay before the first check
    time.sleep(5)

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
                with open(file_path, 'r') as f:
                    combined_results[spider_name] = json.load(f)
                app.logger.info(f"Loaded results for {spider_name}.")
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