import scrapy
from mv_crawler.settings import WEB_TO_CRAWL
from mv_crawler.youtube_handler import add_video
from scrapy.linkextractors import LinkExtractor


class MVSpider(scrapy.Spider):
    name = "mv_spider"

    start_urls = [
        WEB_TO_CRAWL,
    ]

    def parse(self, response, **kwargs):
        print("\n\n\n\nSTARTING TO PARSE\n\n")
        link_extractor = LinkExtractor(allow="youtube.com/watch")

        for link in link_extractor.extract_links(response):
            video_hash = link.url.split("/watch?v=")[1]
            add_video(
                playlist_id="PLyQV_YUFr4MX7vQSmlFy3s_8QruqZfq8c", resource_id=video_hash
            )

        follow_link = response.xpath("//a[contains(., 'Siguiente')]//@href").get()
        if follow_link:
            print(f"\n\nNext link found! legoo {follow_link}")
            next_page = response.urljoin(follow_link)
            yield scrapy.Request(next_page, callback=self.parse)

        print(f"scrappy ended at {response.url}")
