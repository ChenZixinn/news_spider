import scrapy
from gne import GeneralNewsExtractor

from news_spider import items
from warehouse import models
from ..utils.page_util import parse_detail

class NewsHunanSpider(scrapy.Spider):
    name = 'news_hunan'
    source = "湖南在线"
    allowed_domains = ['hunan.voc.com.cn','fc.voc.com.cn', "hsjy.voc.com.cn/"]
    start_urls = ['http://hunan.voc.com.cn/','http://fc.voc.com.cn/', 'https://hsjy.voc.com.cn/']
    # start_urls = ['https://hsjy.voc.com.cn/']

    def parse(self, response):
        """获取页面所有链接，并进入提取内容"""
        a_tags = response.css('a')

        # 遍历每个 <a> 标签，获取链接和文本
        for a_tag in a_tags:
            try:
                link = a_tag.attrib['href']
            except Exception as e:
                # print(e)
                continue
            # 不存在返回
            if not link:
                continue
            # 加入域名
            if "http" not in link:
                link = response.url + link

            # 每个板块的判断逻辑
            channel = ""
            if "fc.voc.com.cn" in response.url:
                channel = "房产"
                if "view" not in link:
                    continue
            elif "hunan.voc.com.cn" in response.url:
                channel = "首页"
                if "article" not in link:
                    continue
            elif "hsjy.voc.com.cn" in response.url:
                channel = "教育"
                if "article" not in link:
                    continue

            # 获取到链接，发起请求获取内容
            try:
                yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True,
                                     meta={"channel":channel, "source":self.source})
            except Exception as e:

                print(e)
                print(f"err url:{link}")

    def parse_page(self, response):
        yield parse_detail(response)



