import json
import re

import scrapy

from news_spider.utils.page_util import parse_detail


class XinhuaSpider(scrapy.Spider):
    name = 'xinhua'
    source = "新华网"
    allowed_domains = ['news.cn']
    start_urls = []
    for i in range(1,51):
        start_urls.append(f"http://da.wa.news.cn/nodeart/page?nid=113351&pgnum={i}&cnt=20&attr=&tp=1&orderby=1&callback=jQuery1124014177163243151725_1688376976111&_=1688376976116")
        start_urls.append(f"http://da.wa.news.cn/nodeart/page?nid=11245930&pgnum={i}&cnt=30&attr=&tp=1&orderby=1&callback=jQuery112406328003490911496_1688393677991&_=1688393677992")

    def start_requests(self):
        # 自定义请求的URL列表
        custom_urls = [
            'http://www.news.cn/fortunepro/youxuan/ds_43faa396ef064f4aa12edd7d0aea12d2.json',
            "http://www.news.cn/worldpro/gjxw/ds_8d5294ed513c4779af6242a3623aa27b.json"
        ]

        # 遍历自定义URL列表，发送请求
        for url in custom_urls:
            yield scrapy.Request(url=url, callback=self.parse_json)

        # 调用原来的start_requests方法，保留原来的start_urls
        yield from super().start_requests()

    def parse_json(self, response):
        data = json.loads(response.text)
        for news in data["datasource"]:

            link = news["publishUrl"]
            if "http" in link:
                if "fortunepro" in response.url:
                    channel = "财经"
                else:
                    channel = "国际"
                yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True,
                                     meta={"channel": channel, "source": self.source})

    def parse(self, response):
        # 使用正则表达式提取最外层括号中的内容
        match = re.search(r'\((.*)\)', response.text)

        # 提取到的内容
        if match:
            content = match.group(1)
            self.logger.debug(f"content:{content}")
            data = json.loads(content)
            for news in data["data"]["list"]:
                link = news["LinkUrl"]
                if "http" in link:
                    if "politics" in link:
                        channel = "时政"
                    else:
                        channel = "首页"

                    yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True, meta={
                        "channel": channel, "source": self.source})

    def parse_page(self, response):
        yield parse_detail(response, self.crawler.redis_client)
