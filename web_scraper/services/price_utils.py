import re

def normalize_price(price_str):
    price_str = re.sub(r'[^\d.]', '', price_str)
    try:
        return float(price_str)
    except ValueError:
        return 0.0
