import os
import json
import re
import logging
from services.price_utils import normalize_price

def combine_and_filter_results(search_term, result_files):
    combined_data = []
    search_keywords = [keyword.strip().lower() for keyword in search_term.split('+')]

    for spider_name, file_name in result_files.items():
        file_path = os.path.join(os.getcwd(), file_name)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    for line in f:
                        try:
                            data = json.loads(line.strip())
                            title = data.get('title', '').lower()
                            price_str = data.get('price', '')

                            if data.get('title') and data.get('price'):
                                price = normalize_price(price_str)

                                if all(re.search(r'\b' + re.escape(keyword) + r'\b', title) for keyword in search_keywords):
                                    combined_data.append(data)
                        except json.JSONDecodeError as e:
                            logging.error(f"Error decoding line in {file_name}: {e}")
            except Exception as e:
                logging.error(f"Error reading {file_name}: {e}")

    combined_data.sort(key=lambda x: normalize_price(x['price']))
    return combined_data
