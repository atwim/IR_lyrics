import scrapy
from string import ascii_lowercase
import time
import json


class azlyrics(scrapy.Spider):
    name = "azlyrics"
    allowed_domains = ["https://www.azlyrics.com","www.azlyrics.com"]
    # start_urls = list(["https://www.azlyrics.com/" + i + ".html" for i in ascii_lowercase])
    start_urls = ["https://www.azlyrics.com/a.html"]

    def parse(self, response):
        for col in response.xpath("html body.margin50 div.container.main-page div.row div.col-sm-6.text-center.artist-col"):
            print(col.get())


# /html/body/div[2]/div/div[2]
# /html/body/div[2]/div/div[2]
# "https://www.azlyrics.com/a/" + song_name + ".html"

#         col-sm-6 text-center artist-col

