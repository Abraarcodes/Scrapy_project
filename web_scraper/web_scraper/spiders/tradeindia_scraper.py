import scrapy

class TradeIndiaSpider(scrapy.Spider):
    name = 'tradeindia'
    allowed_domains = ['tradeindia.com']

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
        # Scraping the title, price, and other data directly from the search result page
        products = response.css('div.mcatsliderwrapper')
        for product in products:
            # Extract title (from the title attribute in the <a> tag)
            title = product.css('h2::text').get()

            # Extract price (assuming it's inside the <strong> tag)
            price = product.css('div.price_and_qty p::text').get()

            # Extract link (from the href attribute in the <a> tag)
            link = product.css('a::attr(href)').get()

            # Ensure the link is a full URL
            full_link = response.urljoin(link) if link else None

            # Format price
            formatted_price = self.format_price(price)

            # Yield the scraped data directly from the search results page
            yield {
                'title': title.strip(),
                'price': price.strip(),
                'rating': 'No rating',
                'url': full_link,  # Include the search result URL
            }

        # Pagination: follow next page if it exists
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def format_price(self, price):
        # This function can be used to clean and format the price data if needed
        if price:
            return price.strip().replace(",", "")
        return 'No price'
