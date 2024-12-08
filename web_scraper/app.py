from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from services.crawler_service import run_crawlers_async, RESULT_FILES
from services.filter_service import combine_and_filter_results
from services.purchase_service import save_purchase
from services.relax_filter import relaxed_combine_and_filter_results

app = Flask(__name__)
CORS(app, resources={r'/scrape': {"origins": ['http://localhost:5173']}, r'/save-purchase': {"origins": ['http://localhost:5173']}})

@app.route('/scrape', methods=['GET'])
def scrape():
    search_term = request.args.get('search', '')
    if not search_term:
        return jsonify({'error': 'No search term provided'}), 400

    for file in RESULT_FILES.values():
        if os.path.exists(file):
            os.remove(file)

    run_crawlers_async(search_term)
    combined_results = combine_and_filter_results(search_term, RESULT_FILES)
    return jsonify(combined_results)



@app.route('/relaxed-scrape', methods=['GET'])
def relaxed_scrape():
    """
    Flask route to initiate scraping with less strict filtering logic.
    """
    search_term = request.args.get('search', '')
    if not search_term:
        return jsonify({'error': 'No search term provided'}), 400

    # Clear old result files
    for file in RESULT_FILES.values():
        if os.path.exists(file):
            os.remove(file)

    # Run the spiders
    run_crawlers_async(search_term)

    # Use the relaxed filtering logic
    combined_results = relaxed_combine_and_filter_results(search_term, RESULT_FILES)
    return jsonify(combined_results)



@app.route('/save-purchase', methods=['POST'])
def save_purchase_route():
    data = request.get_json()
    response = save_purchase(data.get('title'), data.get('price'), data.get('link'))
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
