import os
import json

PURCHASES_FILE = 'purchases.json'

def save_purchase(title, price, link):
    if not title or not price or not link:
        return {'success': False, 'error': 'Missing required fields'}

    purchase_data = {'title': title, 'price': price, 'link': link}
    existing_purchases = []

    if os.path.exists(PURCHASES_FILE):
        with open(PURCHASES_FILE, 'r') as file:
            existing_purchases = json.load(file)

    existing_purchases.append(purchase_data)

    with open(PURCHASES_FILE, 'w') as file:
        json.dump(existing_purchases, file, indent=4)

    return {'success': True}
