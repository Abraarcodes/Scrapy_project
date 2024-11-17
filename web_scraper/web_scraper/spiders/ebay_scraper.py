import scrapy

class EbaySpider(scrapy.Spider):
    name = 'ebay'
    allowed_domains = ['ebay.com']
    start_urls = ['https://www.ebay.com/sch/i.html?_nkw=laptop&_ipg=240']

    custom_settings = {
        # 'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        # 'USER_AGENT':'Mozilla/5.0 (com patible; Gogglebot/2.1; +http://www.google.com/bot.html)',
        'FEED_FORMAT': 'json',
        'FEED_URI': 'ebay_products.json',
    }

    def parse(self, response):
        # Extract product links from the search result page
        product_links = response.css('.s-item__link::attr(href)').getall()[:10]

        for link in product_links:
            yield scrapy.Request(link, callback=self.parse_product)

    def parse_product(self, response):
        
        # Scraping the title and other details
        title = response.css('h1.x-item-title__mainTitle span::text').get() or 'No title'
        price=response.css('div.x-price-primary span::text').get() or 'No price'
        
        # Yield the scraped data (at least the title is required)
        yield {
            'title': title,
            'price':price
        }
