import scrapy


class RanobelibSpider(scrapy.Spider):
    name = "ranobelib"
    allowed_domains = ["ranobelib.me"]
    start_urls = ["https://ranobelib.me/ru/122448--shadow-slave/read/v0/c0?bid=13947"]

    def parse(self, response):
        pass
