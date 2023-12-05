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
    # start_urls = ["https://www.songlyrics.com/a/"]

    # def parse_song_page(self,response):
    #     for


    def parse_get_data(self,response):
        # print("yes")
        # print(response.xpath("//div[@class='pagetitle']/h1[text()]").get())
        return {
            # "title": response.xpath("//div[@class='pagetitle']/h1[text()]").get().split("- ")[1].split(" Lyrics")[0] ,
            "title": response.xpath("//div[@class='pagetitle']/h1[text()]").get() ,
            "genre": response.xpath("//div[@class='pagetitle']//p[3]//a/text()").get() ,
            "artist": response.xpath("//div[@class='pagetitle']//p[1]//a[text()]").get(),
            "lyrics": response.xpath("//p[@class='songLyricsV14 iComment-text'][text()]").get()
        }
    def parse_artist_page(self,response):
        for artist in response.xpath("//tbody/tr/td/a"):
            # print(artist.attrib["href"])
            song_page = artist.attrib["href"]
            # print("here " + song_page)

            yield scrapy.Request(song_page, callback=self.parse_song_page)

    def parse_song_page(self, response):
        for song in response.xpath("//tbody//a"):
            # print(artist.attrib["href"])
            song_page = song.attrib["href"]
            # print("here " + song_page)
            return scrapy.Request(song_page, callback=self.parse_get_data)


    def parse(self, response):
        if response.status == 200:
            yield from self.parse_artist_page(response)
            for load_more_page in response.xpath("//a[text()='Next']"):
                if load_more_page is not None:
                    # print(load_more_page.attrib["href"])
                    next_page = self.allowed_domains[0] + load_more_page.attrib["href"]
                    yield scrapy.Request("https://" + next_page, callback=self.parse)

# /html/body/div[2]/div/div[2]
# /html/body/div[2]/div/div[2]
# "https://www.azlyrics.com/a/" + song_name + ".html"

#         col-sm-6 text-center artist-col

