import scrapy

from mv_crawler.youtube_handler import add_video


class MVSpider(scrapy.Spider):
    name = "mv_spider"

    start_urls = [
        "https://www.mediavida.com/foro/musica/synthwave-omg-im-so-retro-519088",
    ]

    def parse(self, response, **kwargs):
        print(f"Parsing: {response.url}")
        for youtube_link in response.css("div.youtube_lite a::attr(href)").extract():
            try:
                video_hash = youtube_link.split("/watch?v=")[1]
            except IndexError:
                print(f"Cant parse {youtube_link}")
                continue

            add_video(playlist_id="PLyQV_YUFr4MX7vQSmlFy3s_8QruqZfq8c", resource_id=video_hash)
            print(f"\n{youtube_link} added\n")
            # exit()

        follow_link = response.xpath("//a[contains(., 'Siguiente')]//@href").get()
        if follow_link:
            print(f"Next link found! legoo {follow_link}")
            next_page = response.urljoin(follow_link)
            yield scrapy.Request(next_page, callback=self.parse)

        print(f"scrappy ended at {response.url}")


