import scrapy
from string import ascii_lowercase
import time

class musicxmatch(scrapy.Spider):
    name = "musicxmatch"
    allowed_domains = ["https://www.musixmatch.com","www.musixmatch.com"]
    # start_urls = list(["https://www.azlyrics.com/" + i + ".html" for i in ascii_lowercase])
    start_urls = ["https://www.musixmatch.com/explore/genre/Alternative/1"
                  "https://www.musixmatch.com/explore/genre/Blues/1",
                  "https://www.musixmatch.com/explore/genre/Childrens-Music/1",
                  "https://www.musixmatch.com/explore/genre/Christian-Gospel/1",
                  "https://www.musixmatch.com/explore/genre/Classical/1"
                  "https://www.musixmatch.com/explore/genre/Country/1",
                  "https://www.musixmatch.com/explore/genre/Dance/1"]
                  # "https://www.musixmatch.com/explore/genre/Easy-Listening/1",
                  # "https://www.musixmatch.com/explore/genre/Electronic/1",
                  # "https://www.musixmatch.com/explore/genre/Folk/1",
                  # "https://www.musixmatch.com/explore/genre/Hip-Hop-Rap/1",
                  # "https://www.musixmatch.com/explore/genre/Jazz/1",
                  # "https://www.musixmatch.com/explore/genre/Opera/1",
                  # "https://www.musixmatch.com/explore/genre/Pop/1",
                  # "https://www.musixmatch.com/explore/genre/R-B-Soul/1",
                  # "https://www.musixmatch.com/explore/genre/Reggae/1",
                  # "https://www.musixmatch.com/explore/genre/Rock/1",
                  # "https://www.musixmatch.com/explore/genre/Singer-Songwriter/1",
                  # "https://www.musixmatch.com/explore/genre/Soundtrack/1",
                  # "https://www.musixmatch.com/explore/genre/World/1"]

    def parse_get_data(self, response):
        return {
            "title": response.xpath("//h1[@class='mxm-track-title__track ']/text()").get(),
            "artist": response.xpath("//a[@class='mxm-track-title__artist mxm-track-title__artist-link']/text()").get(),
            "lyrics": response.xpath("//div[@class='mxm-lyrics']/span/div/p/span[@class='lyrics__content__ok']/text()").get(),
            "genre": response.url.split("/")[-2]
        }


    def parse_title(self, response):
        for title in response.xpath("//a[@class='title']"):
            if title is not None:
                next_page = self.allowed_domains[0] + title.attrib["href"]
                yield scrapy.Request(next_page, callback=self.parse_get_data)

    def parse(self, response):
        if response.status == 200:
            yield from self.parse_title(response)
            for load_more_page in response.xpath("//a[@class='button page-load-more']"):
                if load_more_page is not None:
                    print(load_more_page.attrib["href"])
                    next_page = self.allowed_domains[0] + load_more_page.attrib["href"]
                    yield scrapy.Request(next_page, callback=self.parse)
