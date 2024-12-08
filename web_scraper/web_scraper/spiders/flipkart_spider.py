import scrapy
from scrapy_splash import SplashRequest
import re

class FlipkartSpider(scrapy.Spider):
    name = 'flipkart'
    allowed_domains = ['flipkart.com', 'localhost']
    # start_urls = ['https://www.flipkart.com/search?q=laptop']
    def __init__(self, search='', *args, **kwargs):
        super(FlipkartSpider, self).__init__(*args, **kwargs)
        # Use the search parameter to dynamically generate the URL
        self.start_urls = [f'https://www.flipkart.com/search?q={search}']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 5}, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })

    def parse(self, response):
        self.logger.info("Parsing Flipkart response...")

        # Get the product links
        product_links = response.css('a.CGtC98::attr(href), a.VJA3rP::attr(href)').getall()
        # self.logger.info(f"Found {len(product_links)} product links.")

        for link in product_links:
            full_url = response.urljoin(link)  # Convert relative URLs to absolute
            yield scrapy.Request(full_url, callback=self.parse_product)

    def parse_product(self, response):
        title=response.css('span.VU-ZEz::text').get()
        price=response.css('div.CxhGGd::text').get()
        if price:
         price = re.sub(r'[^\d]', '', price)
        rating=response.css('div.XQDdHH::text').get()

        yield {
            'title': title.strip() if title else 'No title',
            'price': price,
            'rating': rating.strip() if rating else 'No rating',
            'source':'Flipkart',
            'url': response.url  # Include the product URL
        }
















