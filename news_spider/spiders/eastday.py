import json

import scrapy

from news_spider.utils.page_util import parse_detail


class EastdaySpider(scrapy.Spider):
    name = 'eastday'
    source = "东方网"
    allowed_domains = ['eastday.com']
    start_urls = ['http://eastday.com/']

    def start_requests(self):
        # 自定义请求的URL列表
        custom_urls = [
            # f"https://apin.eastday.com/apiplus/special/specialnewslistbyurl?specialUrl=1632798465040016&skipCount={i*20}&limitCount=20"
            # for i in range(0, 100)
        ]
        for i in range(0, 100):
            custom_urls.append(f"https://apin.eastday.com/apiplus/Special/specialnewslistbyremark?limitCount={i*20}&skipCount=300&remarkIds=14&remarkType=2")
            custom_urls.append(f"https://apin.eastday.com/apiplus/Special/specialnewslistbyremark?limitCount={i*20}&skipCount=20&remarkIds=2&remarkType=2")
            custom_urls.append(f"https://apin.eastday.com/apiplus/Special/specialnewslistbyremark?limitCount=20&skipCount={i*20}&remarkIds=1&remarkType=2")
            custom_urls.append(f"https://apin.eastday.com/apiplus/Special/specialnewslistbyremark?limitCount=20&skipCount={i*20}&remarkIds=5&remarkType=2")
            custom_urls.append(f"https://apin.eastday.com/apiplus/special/specialnewslistbyurl?specialUrl=1589867129016093&skipCount={i*20}&limitCount=20")
            custom_urls.append(f"https://apin.eastday.com/apiplus/special/specialnewslistbyurl?specialUrl=1685349427350001&skipCount=20&limitCount={i*20}")

        # 遍历自定义URL列表，发送请求
        for url in custom_urls:
            yield scrapy.Request(url=url, callback=self.parse_json)

        # 调用原来的start_requests方法，保留原来的start_urls
        yield from super().start_requests()

    def parse_json(self, response):
        data = json.loads(response.text)
        for news in data["data"]["list"]:
            link = news["url"]
            images = news["imgUrl"]
            channel = data["data"].get("title")
            if not channel:
                if "remarkIds=14" in response.url:
                    channel = "国内"
                elif "remarkIds=2" in response.url:
                    channel = "国际"
                elif "remarkIds=1" in response.url:
                    channel = "财经"
                elif "remarkIds=5" in response.url:
                    channel = "军事"
                elif "specialUrl=1589867129016093" in response.url:
                    channel = "评论"
            self.logger.debug(f"link:{link}, images:{images}, channel:{channel}")
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True,
                                 meta={"channel": channel, "source": self.source, "images": images})

    def parse(self, response):
        pass

    def parse_page(self, response):
        yield parse_detail(response, self.crawler.redis_client)
        # pass

