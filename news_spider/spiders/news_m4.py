import scrapy
from gne import GeneralNewsExtractor

from news_spider import items
from news_spider.utils.page_util import parse_detail
from warehouse import models


class NewsM4Spider(scrapy.Spider):
    name = 'news_m4'
    source = "四月网"
    allowed_domains = ['news.m4.cn', 'mil.m4.cn']
    start_urls = ['http://news.m4.cn/','http://www.m4.cn/']
    # start_urls = []
    for i in range(10):
        # 军事
        start_urls.append(f'http://mil.m4.cn/list_{i+1}.shtml')
        # 社会
        start_urls.append(f'http://news.m4.cn/society/list_{i+1}.shtml')
    for i in range(100):
        # 财经
        start_urls.append(f'http://news.m4.cn/finance/list_{i+1}.shtml')

    def parse(self, response):
        """ 找到页面中的新闻链接，发送给下一次请求 """
        a_tags = response.css('a')

        # 遍历每个 <a> 标签，获取链接和文本
        for a_tag in a_tags:
            try:
                link = a_tag.attrib['href']
            except Exception as e:
                # print(e)
                continue
            if "html" not in link or 'about' in link or 'sitemap' in link or 'link' in link or 'bbs' in link:
                continue
            # print(link)
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True)

    def parse_page(self, response):
        channel = response.xpath('/html/body/div[4]/div/div/div[1]/div/div/div/div[1]/div[1]/div/div/span[2]/a[3]/text()').extract_first()
        if not channel:
            channel = "首页"
        # if not channel:
        #     print(response.url)
        response.meta["source"] = self.source
        response.meta["channel"] = channel

        yield parse_detail(response, self.crawler.redis_client)

