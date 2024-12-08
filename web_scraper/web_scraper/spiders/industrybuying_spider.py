import scrapy
from scrapy_splash import SplashRequest
import re

class IndustrybuyingSpider(scrapy.Spider):
    name = 'industrybuying'
    allowed_domains = ['industrybuying.com', 'localhost']
    # start_urls = ['https://www.industrybuying.com/search/?q=']  # Example URL

    def __init__(self, search='', *args, **kwargs):
        super(IndustrybuyingSpider, self).__init__(*args, **kwargs)
        # Use the search parameter to dynamically generate the URL
        self.start_urls = [f'https://www.industrybuying.com/search?q={search}']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 5}, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })

    def parse(self, response):
        self.logger.info("Parsing Industrybuying response...")

        # Extract each product card
        products = response.css('product-card')
        for product in products:
            # Extract title (from the title attribute in the <a> tag)
            title = product.css('a::attr(title)').get()

            # Extract price (assuming it's inside the <strong> tag)
            price = product.css('strong::text').get()

            # Extract link (from the href attribute in the <a> tag)
            link = product.css('a::attr(href)').get()

            # Ensure the link is a full URL
            full_link = response.urljoin(link) if link else None

            # Format price
            formatted_price = self.format_price(price)

            yield {
                'title': title,
                'price': formatted_price,
                'rating': 'No rating',  # Adjust if there's a rating selector available
                'source': 'Industry Buying',
                'url': full_link
            }

    def format_price(self, price):
        # Clean unwanted characters (like â‚¹) and extra whitespaces
        cleaned_price = re.sub(r'[^\d,-]', '', price.strip())

        # Check if there is a price range (indicated by '-')
        if '-' in cleaned_price:
            # If there is a range, split and format both parts
            price_range = cleaned_price.split('-')
            price_range = [self.format_number(p.strip()) for p in price_range]
            return '-'.join(price_range)
        else:
            # Single price, just format it
            return self.format_number(cleaned_price)

    def format_number(self, number):
        # Remove commas, if present, before converting to integer
        number = number.replace(',', '')
        # Format the number with commas (e.g., 69999 -> 69,999)
        return '{:,}'.format(int(number))
