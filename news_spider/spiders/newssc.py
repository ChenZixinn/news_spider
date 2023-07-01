import scrapy
from gne import GeneralNewsExtractor

from news_spider import items
from news_spider.utils.page_util import parse_detail
from warehouse import models


class NewsscSpider(scrapy.Spider):
    name = 'newssc'
    source = "四川新闻"
    allowed_domains = ['newssc.org']
    start_urls = ['http://newssc.org/', 'http://www.scjyxww.com.cn/','http://finance.newssc.org/']

    def parse(self, response):
        a_tags = response.css('a')

        # 遍历每个 <a> 标签，获取链接和文本
        for a_tag in a_tags:
            try:
                link = a_tag.attrib['href']
            except Exception as e:
                # print(e)
                continue
            if 'html' not in link or 'about' in link or 'mala' in link or 'index' in link:
                continue
            # print(link)
            yield scrapy.Request(link, callback=self.parse_detail, encoding="utf-8", dont_filter=True)

    def parse_detail(self, response):
        # 教育网的频道位置不同,根据url直接判断为教育频道
        if "scjyxww" in response.url:
            channel = "教育"
        elif 'finance' in response.url:
            channel = "财政"
        else:
            channel = response.xpath('/html/body/main/div/div[1]/a[2]/text()').extract_first()
        if not channel:
            # print(f"未搜索到频道:{response.url}")
            channel = '首页'
        # else:
        #     print(f"channel:{channel}")
        response.meta["source"] = self.source
        response.meta["channel"] = channel
        yield parse_detail(response)

