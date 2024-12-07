# import scrapy

# class IndustrybuyingSpider(scrapy.Spider):
#     name = 'industrybuying'
#     allowed_domains = ['industrybuying.com','localhost']
#     start_urls = ['https://www.industrybuying.com/search/?q=laptop+asus+tuf']  # Example URL

#     def parse(self, response):
#         self.logger.info("Parsing Industrybuying response...")

#         # Extract each product card
#         products = response.css('product-card')[:3]
#         for product in products:
#             # Extract title (from the title attribute in the <a> tag)
#             title = product.css('a::attr(title)').get()
            
#             # Extract price (assuming it's inside the <strong> tag)
#             price = product.css('strong::text').get()

#             # Extract link (from the href attribute in the <a> tag)
#             link = product.css('a::attr(href)').get()

#             yield {
#                 'title': title,
#                 'price': price,
#                 'rating':'No rating',
#                 'source':'Industry Buying',
#                 'url': link
#             }



import scrapy
import re

class IndustrybuyingSpider(scrapy.Spider):
    name = 'industrybuying'
    allowed_domains = ['industrybuying.com', 'localhost']
    start_urls = ['https://www.industrybuying.com/search/?q=laptop+asus+tuf']  # Example URL

    def parse(self, response):
        self.logger.info("Parsing Industrybuying response...")

        # Extract each product card
        products = response.css('product-card')[:3]
        for product in products:
            # Extract title (from the title attribute in the <a> tag)
            title = product.css('a::attr(title)').get()

            # Extract price (assuming it's inside the <strong> tag)
            price = product.css('strong::text').get()

            # Extract link (from the href attribute in the <a> tag)
            link = product.css('a::attr(href)').get()

            # Format price
            formatted_price = self.format_price(price)

            yield {
                'title': title,
                'price': formatted_price,
                'rating': 'No rating',  # Adjust if there's a rating selector available
                'source': 'Industry Buying',
                'url': link
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
