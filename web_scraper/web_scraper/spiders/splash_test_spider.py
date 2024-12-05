import scrapy
from scrapy_splash import SplashRequest


class SplashTestSpider(scrapy.Spider):
    name = 'splash_test'

    # The website to scrape (example: a JS-rendered page)
    start_urls = ['https://quotes.toscrape.com/js/']  # This website is JS-rendered

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url=url,
                callback=self.parse,
                args={'wait': 2},  # Splash will wait 2 seconds before returning the rendered page
            )

    def parse(self, response):
        # Extract quotes and authors from the JS-rendered page
        quotes = response.css('div.quote')
        for quote in quotes:
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
