import scrapy
from string import ascii_lowercase
import time
import json


class lyricfind(scrapy.Spider):
    name = "lyricfind"
    # allowed_domains = ["https://lyrics.lyricfind.com"]
    start_urls = list(["https://lyrics.lyricfind.com/browse/" + i for i in ascii_lowercase])
    # start_urls = list(["https://lyrics.lyricfind.com/browse/a"])
    page = 1

    def parse_get_data(self, response):
        jsonresponse = json.loads(response.text)
        # print(jsonresponse["pageProps"]["artist"])
        return {
            "title": jsonresponse["pageProps"]["songData"]["track"]["title"],
            "artist": jsonresponse["pageProps"]["artist"],
            "lyrics": jsonresponse["pageProps"]["songData"]["track"]["lyrics"]
            # "genre": response.url.split("/")[-2]
        }

    # def parse_song(self, response):
    #     for title in response.xpath("//a[@class='MuiTypography-root MuiTypography-body2 css-fzl7rz']"):
    #         if title is not None:
    #             next_page = self.allowed_domains[0] + title.attrib["href"]
    #             yield scrapy.Request(next_page, callback=self.parse_get_data)

    def parse_aux(self, response):
        if response.status == 200:
            letter = response.url.split("letter=")[1].split("&")[0]
            jsonresponse = json.loads(response.text)
            for track in jsonresponse["tracks"]:


                #replace spaces with -
                title = " ".join(track["title"].split())
                artist = " ".join(track["artist"]["name"].split())

                # take the name of the artist before the and
                if len(artist.split("and")) > 1:
                    artist = artist.split("and")[0][:-1]


                title = title.lower().replace(" ", "-")
                artist = artist.lower().replace(" ", "-")

                id = artist + "-" + title

                url = f'https://lyrics.lyricfind.com/_next/data/ruqb0mkwHRwCTAAbYcEET/en-US/lyrics/{id}.json?songId={id}'
                yield scrapy.Request(url=url, callback=self.parse_get_data)
                # print(artist)
                # print(title)
            self.page += 1
            url = f'https://lyrics.lyricfind.com/api/v1/metadata?reqtype=listlyrics&letter={letter}&limit=20&territory=CH&output=json&offset={140*self.page}'
            yield scrapy.Request(url=url, callback=self.parse_aux)




    def parse(self, response):
        letter = response.url.split("/")[-1]
        url = f'https://lyrics.lyricfind.com/api/v1/metadata?reqtype=listlyrics&letter={letter}&limit=20&territory=CH&output=json&offset=140'
        yield scrapy.Request(url=url, callback=self.parse_aux)
        for song in response.xpath("//div[@class='MuiBox-root css-18hgwaj']/a[@class='css-11g9kr1']"):
            # print(song.attrib["href"])
            if song is not None:
                # next_page = "https://lyrics.lyricfind.com" + song.attrib["href"]
                url = f'https://lyrics.lyricfind.com/_next/data/ruqb0mkwHRwCTAAbYcEET/en-US/lyrics/{song.attrib["href"].split("/")[2]}.json?songId={song.attrib["href"].split("/")[2]}'
                # url = f'https://lyrics.lyricfind.com /_next/data/ruqb0mkwHRwCTAAbYcEET/en-US/lyrics/ michael - skerbec - a.json?songId = michael - skerbec - a
                yield scrapy.Request(url=url, callback=self.parse_get_data)
        url = f'https://lyrics.lyricfind.com/api/v1/metadata?reqtype=listlyrics&letter={letter}&limit=20&territory=CH&output=json&offset=140'
        yield scrapy.Request(url=url, callback=self.parse)
