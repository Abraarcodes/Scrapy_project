# import scrapy
# from scrapy_splash import SplashRequest

# class ProductSpider(scrapy.Spider):
#     name = 'amazon'
#     allowed_domains = ['amazon.in','localhost']
#     start_urls = ['https://www.amazon.in/s?k=laptop']

#     def start_requests(self):
#         for url in self.start_urls:
#             yield SplashRequest(url, self.parse, args={'wait': 2})

#     def parse(self, response):
#         # Extract product details here
#         products = response.css('div.s-result-item')

#         for product in products:
#             title = product.css('h2 a span::text').get()
#             price = product.css('span.a-price span.a-offscreen::text').get()
#             image_url = product.css('img.s-image::attr(src)').get()
#             product_url = product.css('h2 a::attr(href)').get()

#             yield {
#                 'title': title,
#                 'price': price,
#                 'image_url': image_url,
#                 'product_url': response.urljoin(product_url)
#             }

#             # Follow pagination link
#             next_page = response.css('li.a-last a::attr(href)').get()
#             if next_page:
#                 yield SplashRequest(response.urljoin(next_page), self.parse, args={'wait': 2})



import scrapy
from scrapy_splash import SplashRequest

class AmazonDeliverySpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.in','localhost']
    start_urls = ['https://www.amazon.in/s?k=laptop']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 5}, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })


    def parse(self, response):
    # Save the response to a file for inspection
        with open('response.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
    
    # Now try extracting the delivery info
        delivery_info = response.css('span.nav-line-1.nav-progressive-content::text').get()
    
        if delivery_info:
            yield {'delivery_info': delivery_info.strip()}
        else:
            self.log("Delivery info not found!")

