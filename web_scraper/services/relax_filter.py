import os
import json
import re
import logging
from services.price_utils import normalize_price

def relaxed_combine_and_filter_results(search_term, result_files):
    """
    Combines data from individual spider result files with less strict filtering logic.
    Includes results if at least some keywords from the search term appear in the title.
    """
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

                            # Check if title and price are present
                            if data.get('title') and data.get('price'):
                                price = normalize_price(price_str)

                                # Count matching keywords
                                match_count = sum(1 for keyword in search_keywords if keyword in title)

                                # Include if at least half of the keywords match
                                if match_count >= len(search_keywords) / 2:
                                    combined_data.append(data)
                        except json.JSONDecodeError as e:
                            logging.error(f"Error decoding line in {file_name}: {e}")
            except Exception as e:
                logging.error(f"Error reading {file_name}: {e}")

    # Sort by price (low to high)
    combined_data.sort(key=lambda x: normalize_price(x['price']))
    return combined_data
