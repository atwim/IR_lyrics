import scrapy
from string import ascii_lowercase
import time
import json
from scraper_api import ScraperAPIClient
# client = ScraperAPIClient('fd02e69c75265d064719fc84e866b159')


class songlyrics(scrapy.Spider):
    name = "songlyrics"
    rotate_user_agent = True
    allowed_domains = ["www.songlyrics.com"]
    start_urls = list(["https://www.songlyrics.com/" + i + "/" for i in ascii_lowercase])
    # start_urls = ["https://www.songlyrics.com/acoustic-lyrics.php"]

    # def parse_song_page(self,response):
    #     for
    def parse_artist_page(self,response):
        for artist in response.xpath("//tbody/tr/td/a"):
            # print(artist.attrib["href"])
            song_page = artist.attrib["href"]
            yield scrapy.Request(song_page, callback=self.parse_song_page)

    def parse_get_data(self,response):
        return {
            "title": response.xpath("//div[@class='col-xs-12 col-lg-8 text-center']/b[1]").get() ,
            "artist": response.xpath("//div[@class='lyricsh']//b").get(),
            "lyrics": response.xpath("//div[@class='col-xs-12 col-lg-8 text-center']/div[5]").get()
        }

    def parse(self, response):
        if response.status == 200:
            yield from self.parse_artist_page(response)
            for load_more_page in response.xpath("//a[text()='Next']"):
                if load_more_page is not None:
                    print(load_more_page.attrib["href"])
                    next_page = self.allowed_domains[0] + load_more_page.attrib["href"]
                    yield scrapy.Request(next_page, callback=self.parse)

# /html/body/div[2]/div/div[2]
# /html/body/div[2]/div/div[2]
# "https://www.azlyrics.com/a/" + song_name + ".html"

#         col-sm-6 text-center artist-col

