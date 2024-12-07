import scrapy
from scrapy_splash import SplashRequest
import re

class IndustrybuyingSpider(scrapy.Spider):
    name = 'industrybuying'
    allowed_domains = ['industrybuying.com', 'localhost']
    
    def __init__(self, search='', *args, **kwargs):
        super(IndustrybuyingSpider, self).__init__(*args, **kwargs)
        # Use the search parameter to dynamically generate the URL
        self.start_urls = [f'https://www.industrybuying.com/search/?q={search}']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 5}, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })

    def parse(self, response):
        self.logger.info("Parsing Industrybuying response...")

        # Get the product links
        product_links = response.css('div.grow a::attr(href)').getall()

        for link in product_links:
            full_url = response.urljoin(link)  # Convert relative URLs to absolute
            yield scrapy.Request(full_url, callback=self.parse_product)

    def parse_product(self, response):
        # title = response.css('h1.leading-[20px]::text').get()
        title = response.css('h1.leading-\\[20px\\]::text').get()
        price = response.xpath('//product-price-summary//div[contains(@class, "text-[#535353]")]/text()').get()
        
        if price:
            price = re.sub(r'[^\d]', '', price)  # Remove non-numeric characters
        rating = response.css('span.product-rating__value::text').get()

        yield {
            'title': title.strip() if title else 'No title',
            'price': price,
            'rating': rating.strip() if rating else 'No rating',
            'url': response.url  # Include the product URL
        }
