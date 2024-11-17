import scrapy

class IndiamartSpider(scrapy.Spider):
    name = 'indiamart'
    allowed_domains = ['indiamart.com']
    start_urls = ['https://dir.indiamart.com/search.mp?ss=samsung&v=4&mcatid=&catid=&tags=res:RC5|ktp:N0|stype:attr=1|mtp:G|wc:1|qr_nm:gd|cs:8742|com-cf:nl|ptrs:na|mc:11352|cat:57|qry_typ:P|lang:en|flavl:10']

    custom_settings = {
        # 'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        # 'USER_AGENT':'Mozilla/5.0 (com patible; Gogglebot/2.1; +http://www.google.com/bot.html)',
        'FEED_FORMAT': 'json',
        'FEED_URI': 'indiamart_products.json',
    }

    def parse(self, response):
        self.logger.info("Parsing Indiamart response...")
        product_links = response.css('.cardlinks::attr(href)').getall()[:10]
        self.logger.info(f"Found {len(product_links)} product links.")

        for link in product_links:
            self.logger.info(f"Processing link: {link}")
            yield scrapy.Request(link, callback=self.parse_product)

    def parse_product(self, response):
        title = response.css('h1.bo.center-heading.centerHeadHeight::text').get() or 'No title'
        price = response.css('span.bo.price-unit::text').get() or 'No price'
        self.logger.info(f"Scraped product: Title: {title}, Price: {price}")
        yield {
        'title': title,
        'price': price
    }
