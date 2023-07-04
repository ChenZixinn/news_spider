import json

import scrapy

from news_spider.utils.page_util import parse_detail


class StnnSpider(scrapy.Spider):
    name = 'stnn'
    source = "星岛环球"
    allowed_domains = ['stnn.cn']
    start_urls = []
    for i in range(0, 100):
        start_urls.append(f"https://www.stnn.cc/api/front/contents?siteID=1&pageIndex={i}&isPreview=false&contentType=&sortType=OrderFlag&attributes=&catalogID=2105&pageSize=20")
        start_urls.append(f"https://www.stnn.cc/api/front/contents?siteID=1&pageIndex={i}&isPreview=false&contentType=&sortType=OrderFlag&attributes=&catalogID=2106&pageSize=20")
        start_urls.append(f"https://www.stnn.cc/api/front/contents?siteID=1&pageIndex={i}&isPreview=false&contentType=&sortType=OrderFlag&attributes=&catalogID=2107&pageSize=20")
        start_urls.append(f"https://www.stnn.cc/api/front/contents?siteID=1&pageIndex={i}&isPreview=false&contentType=&sortType=OrderFlag&attributes=&catalogID=2102&pageSize=20")
        start_urls.append(f"https://www.stnn.cc/api/front/contents?siteID=1&pageIndex={i}&isPreview=false&contentType=&sortType=OrderFlag&attributes=&catalogID=2103&pageSize=20")
        start_urls.append(f"https://www.stnn.cc/api/front/contents?siteID=1&pageIndex={i}&isPreview=false&contentType=&sortType=OrderFlag&attributes=&catalogID=2104&pageSize=20")

    def parse(self, response):
        data = json.loads(response.text)
        channel = ""
        if "catalogID=2105" in response.url:
            channel = "要闻"
        elif "catalogID=2106" in response.url:
            channel = "社会"
        elif "catalogID=2107" in response.url:
            channel = "财经"
        elif "catalogID=2102" in response.url:
            channel = "国际要闻"
        elif "catalogID=2103" in response.url:
            channel = "国际社会"
        elif "catalogID=2104" in response.url:
            channel = "国际财经"
        for news in data["data"]["data"]:
            link = "https://www.stnn.cc" + news["link"]
            # self.logger.debug(f"频道:{channel},link= {link}")
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True,
                                 meta={"channel": channel})

    def parse_page(self, response):
        response.meta["source"] = self.source

        yield parse_detail(response, self.crawler.redis_client)
