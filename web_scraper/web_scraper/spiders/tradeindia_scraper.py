# import scrapy

# class TradeIndiaSpider(scrapy.Spider):
#     name = 'tradeindia'
#     allowed_domains = ['tradeindia.com']

#     def __init__(self, search='', *args, **kwargs):
#         super(TradeIndiaSpider, self).__init__(*args, **kwargs)
#         self.start_urls = [
#             f'https://www.tradeindia.com/search.html?q={search}'
#         ]
#         # Configure logging
#         self.logger.setLevel('DEBUG')  # Ensure debug level logging is enabled

#     custom_settings = {
#         'FEED_FORMAT': 'json',
#         'FEED_URI': 'tradeindia_products.json',
#     }

#     def parse(self, response):
#         self.logger.info("Parsing TradeIndia response...")

#         # Get the product links
#         product_links = response.css('div.product_details a::attr(href)').getall()[:10]
#         self.logger.info(f"Found {len(product_links)} product links.")

#         for link in product_links:
#             full_url = response.urljoin(link)  # Convert relative URLs to absolute
#             self.logger.info(f"Processing link: {full_url}")
#             yield scrapy.Request(full_url, callback=self.parse_product)

#     def parse_product(self, response):
#         # Extracting product details
#         title = response.css('h1.sc-3b1eb120-3.gfjxaV.m-0.Headline3.w-break::text').get() or 'No title'
#         price = response.css('h2.sc-3b1eb120-3.kNXpLP.prPrice.Headline3::text').get() or 'No price'

#         # Logging scraped details for debugging
#         self.logger.info(f"Scraped product: Title: {title}, Price: {price}")

#         yield {
#             'title': title.strip() if title else 'No title',
#             'price': price.strip() if price else 'No price',
#             'url': response.url  # Include the product URL
#         }






# import scrapy

# class TradeIndiaSpider(scrapy.Spider):
#     name = 'tradeindia'
#     allowed_domains = ['tradeindia.com']
#     start_urls = ['https://www.tradeindia.com/search.html?keyword=phone']

#     custom_settings = {
#         # 'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#         # 'USER_AGENT':'Mozilla/5.0 (com patible; Gogglebot/2.1; +http://www.google.com/bot.html)',
#         'FEED_FORMAT': 'json',
#         'FEED_URI': 'tradeindia_products.json',
#     }

#     def parse(self, response):
#         # Extract product links from the search result page
#         product_links = response.css('div.product_details a::attr(href)').getall()[:10]
#         print(product_links)
#         for link in product_links:
#             yield scrapy.Request(link, callback=self.parse_product)

#     def parse_product(self, response):
        
#         # Scraping the title and other details
#         title = response.css('h2.gfjxaV::text').get() or 'No title'
#         price = response.css('h2.sc-3b1eb120-3.kNXpLP.prPrice.Headline3::text').get() or 'No price'
        
#         # Yield the scraped data (at least the title is required)
#         yield {
#             'title': title,
#             'price':price,
            
#         }








import scrapy

class TradeIndiaSpider(scrapy.Spider):
    name = 'tradeindia'
    allowed_domains = ['tradeindia.com']
    start_urls = ['https://www.tradeindia.com/search.html?keyword=samsung+galaxy+tab+3']

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'tradeindia_products.json',
    }

    def parse(self, response):
        # Extract product links from the search result page
        product_links = response.css('div a::attr(href)').getall()[:10]

        # Use response.urljoin to make sure links are absolute
        product_links = [response.urljoin(link) for link in product_links]

        # Print out the correct product links for debugging
        self.logger.info(f"Found {len(product_links)} product links on this page: {product_links}")

        # Follow each product link
        for link in product_links:
            yield scrapy.Request(link, callback=self.parse_product)

    def parse_product(self, response):
        # Scraping the title and price from the product page
        title = response.css('h2.sc-3b1eb120-12.fbCxbT.mb-1.card_title.Body3R::text').get() or 'No title'
        price = response.css('p.sc-3b1eb120-13.bQfzKW.Body3R::text').get() or 'No price'
        
        # Yield the scraped data
        yield {
            'title': title.strip(),
            'price': price.strip(),
            'url': response.url  # Include the product URL in the output
        }
