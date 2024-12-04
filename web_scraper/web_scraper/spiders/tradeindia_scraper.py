
import scrapy

class TradeIndiaSpider(scrapy.Spider):
    name = 'tradeindia'
    allowed_domains = ['tradeindia.com']
    # start_urls = ['https://www.tradeindia.com/search.html?keyword=samsung+galaxy+tab+3']
    
    def __init__(self, search='', *args, **kwargs):
        super(TradeIndiaSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            f'https://www.tradeindia.com/search.html?keyword={search}'
        ]
        # Configure logging
        self.logger.setLevel('DEBUG')
    custom_settings = {
        'FEED_FORMAT': 'jsonlines',
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
        rating=response.css('div.fs13 span.bo.color') or 'No rating'
        
        # Yield the scraped data
        yield {
            'title': title.strip(),
            'price': price.strip(),
            'rating':rating.strip(),
            'url': response.url  # Include the product URL in the output
        }
