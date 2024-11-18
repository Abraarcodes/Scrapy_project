import scrapy

class IndiamartSpider(scrapy.Spider):
    name = 'indiamart'
    allowed_domains = ['indiamart.com']

    def __init__(self, search='', *args, **kwargs):
        super(IndiamartSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            f'https://dir.indiamart.com/search.mp?ss={search}&v=4'
        ]
        # Configure logging
        self.logger.setLevel('DEBUG')  # Ensure debug level logging is enabled

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'indiamart_products.json',
    }

    def parse(self, response):
        self.logger.info("Parsing Indiamart response...")

        # Get the product links
        product_links = response.css('.cardlinks::attr(href)').getall()[:10]
        self.logger.info(f"Found {len(product_links)} product links.")

        for link in product_links:
            full_url = response.urljoin(link)  # Convert relative URLs to absolute
            self.logger.info(f"Processing link: {full_url}")
            yield scrapy.Request(full_url, callback=self.parse_product)

    def parse_product(self, response):
        # Extracting product details
        title = response.css('h1.bo.center-heading.centerHeadHeight::text').get() or 'No title'
        price = response.css('div.fs18 span.bo.price-unit::text').get() or 'No price'

        # Logging scraped details for debugging
        self.logger.info(f"Scraped product: Title: {title}, Price: {price}")

        yield {
            'title': title.strip() if title else 'No title',
            'price': price.strip() if price else 'No price',
            'url': response.url  # Include the product URL
        }
