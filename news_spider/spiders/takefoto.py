import scrapy

from news_spider.utils.page_util import parse_detail, check_link


class TakefotoSpider(scrapy.Spider):
    name = 'takefoto'
    source = "北晚在线"
    allowed_domains = ['takefoto.cn']
    start_urls = ['https://www.takefoto.cn/inland/', "https://www.takefoto.cn/society/","https://www.takefoto.cn/beijing/",
                  "https://www.takefoto.cn/world/", "https://www.takefoto.cn/recreation/", "https://www.takefoto.cn/sports/",
                  "https://www.takefoto.cn/travel/", "https://www.takefoto.cn/industry/", "https://www.takefoto.cn/survey/",
                  "https://www.takefoto.cn/automobile/", "https://www.takefoto.cn/cate/", "https://www.takefoto.cn/health/",
                  "https://www.takefoto.cn/consumption/"]

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
            if link.startswith("//"):
                link = "https:" + link
            exclude = []
            include = ["shtml", 'news']
            if not check_link(link, include, exclude):
                continue
            # print(link)
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True)

    def parse_page(self, response):
        channel = response.xpath('//a[contains(@class, "curmbs__class")]/text()').extract_first()
        response.meta["source"] = self.source
        response.meta["channel"] = channel
        yield parse_detail(response, self.crawler.redis_client)
