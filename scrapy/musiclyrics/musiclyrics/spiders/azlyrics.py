import scrapy
from string import ascii_lowercase
import time
import json


class azlyrics(scrapy.Spider):
    name = "azlyrics"
    rotate_user_agent = True
    allowed_domains = ["www.azlyrics.com"]
    # start_urls = list(["https://www.azlyrics.com/" + i + ".html" for i in ascii_lowercase])
    start_urls = ["https://www.azlyrics.com/a.html"]


    def parse_artist_page(self,response):
        for song_title in response.xpath("//div[@class='listalbum-item']/a"):
            print(song_title.attrib["href"])
            song_page = "https://" + self.allowed_domains[0] + song_title.attrib["href"]
            yield scrapy.Request(song_page, callback=self.parse_get_data)

    def parse_get_data(self,response):
        return {
            "title": response.xpath("//div[@class='col-xs-12 col-lg-8 text-center']/b[1]").get() ,
            "artist": response.xpath("//div[@class='lyricsh']//b").get(),
            "lyrics": response.xpath("//div[@class='col-xs-12 col-lg-8 text-center']/div[5]").get()
        }

    def parse(self, response):
        for title in response.xpath("//div[@class='col-sm-6 text-center artist-col']/a"):
            artist_page = "https://" + self.allowed_domains[0] + "/" + title.attrib["href"]
            yield scrapy.Request(artist_page, callback=self.parse_artist_page)


# /html/body/div[2]/div/div[2]
# /html/body/div[2]/div/div[2]
# "https://www.azlyrics.com/a/" + song_name + ".html"

#         col-sm-6 text-center artist-col

