import time

import w3lib.html

import scrapy
from scrapy.http import Response

class RanobelibSpider(scrapy.Spider):
    name = "ranobelib"
    allowed_domains = ["ranobelib.me"]
    start_urls = ["https://old.ranobelib.me/old/122448--shadow-slave/read/v1/c1?bid=13303"]
    __time_gap = 1  # time for sleep between requests

    @staticmethod
    def __make_text_pretty(text) -> str:
        text = w3lib.html.remove_tags(text)
        text = w3lib.html.replace_escape_chars(text)
        return text

    def parse(self, response: Response, **kwargs):
        text = response.css(".reader-container>p").getall()
        text = "\n".join(self.__make_text_pretty(p) for p in text)
        chapter = response.css(".reader-header-action__text").getall()[1]
        chapter = self.__make_text_pretty(chapter).replace("  ", "")

        yield {
            "chapter": chapter,
            "text": text,
        }

        time.sleep(self.__time_gap)

        next_page = response.css(".button_label_right::attr(href)").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

        # filename = f"shadow-slave.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")
