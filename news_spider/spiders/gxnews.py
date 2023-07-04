import json
import re
import time

import scrapy

from news_spider.utils.page_util import parse_detail


class GxnewsSpider(scrapy.Spider):
    name = 'gxnews'
    source = "广西新闻网"
    allowed_domains = ['gxnews.com.cn']
    start_urls = []
    for i in range(50):
        start_urls.append(f"https://v.gxnews.com.cn/index.php?c=www&a=getArticles&sortids=191&start={i*20}&detail=1&callback=morelist&_={time.time()*1000}")
        start_urls.append(f"https://v.gxnews.com.cn/index.php?c=www&a=getArticles&sortids=12162&start={i*20}&detail=1&callback=morelist&_={time.time()*1000}")
        start_urls.append(f"https://v.gxnews.com.cn/index.php?c=www&a=getArticles&sortids=534&start={i*20}&detail=1&callback=morelist&_={time.time()*1000}")
        start_urls.append(f"https://v.gxnews.com.cn/index.php?c=www&a=getArticles&sortids=46121&start={i*20}&detail=1&callback=morelist&_={time.time()*1000}")
        start_urls.append(f"https://v.gxnews.com.cn/index.php?c=www&a=getArticles&sortids=805&start={i*20}&detail=1&callback=morelist&_={time.time()*1000}")

    def parse(self, response):

        # 从字符串中提取有效的 JSON 部分
        json_str = re.search(r'\[.*\]', response.text).group()

        # 将提取到的 JSON 字符串转换为 Python 对象
        data = json.loads(json_str)

        for news in data:
            link = news["url"]
            if "mk.haiwainet.cn" not in link:
                yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True,
                                     meta={"source": self.source})

    def parse_page(self, response):
        channel = response.xpath("//td[contains(@class, 'article-nav')]/a[last()]/text()").extract_first()
        if not channel:
            channel = response.xpath("//div[contains(@class, 'more-title')]/span/a[last()]/text()").extract_first()
            if not channel:
                channel = response.xpath("//div[contains(@class, 'article-nav')]/a[last()]/text()").extract_first()
        if not channel:
            self.logger.error(f"频道为：{channel}, url:{response.url}")
        response.meta["channel"] = channel
        yield parse_detail(response, self.crawler.redis_client)

