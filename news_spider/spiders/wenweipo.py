import scrapy

from news_spider.utils.page_util import parse_detail


class WenweipoSpider(scrapy.Spider):
    name = 'wenweipo'
    source = "香港文汇网"
    allowed_domains = ['wenweipo.com']
    start_urls = []
    for i in range(1, 51):
        start_urls.append(f"https://www.wenweipo.com/todaywenwei/whHK/more_{i}.html")
        start_urls.append(f"https://www.wenweipo.com/todaywenwei/whmainland/more_{i}.html")
        start_urls.append(f"https://www.wenweipo.com/todaywenwei/whinternational/more_{i}.html")
        start_urls.append(f"https://www.wenweipo.com/todaywenwei/whTW/more_{i}.html")
        start_urls.append(f"https://www.wenweipo.com/todaywenwei/economic/more_{i}.html")
        start_urls.append(f"https://www.wenweipo.com/todaywenwei/investmentandfinancial/more_{i}.html")
        start_urls.append(f"https://www.wenweipo.com/todaywenwei/financialhotspot/more_{i}.html")
        start_urls.append(f"https://www.wenweipo.com/todaywenwei/whphysicaleducation/more_{i}.html")
        start_urls.append(f"https://www.wenweipo.com/todaywenwei/whentertainment/more_{i}.html")

    def parse(self, response):
        channel = ""
        if "mainland" in response.url:
            channel = "内地"
        elif "whHK" in response.url:
            channel = "香港"
        elif "whinternational" in response.url:
            channel = "国际"
        elif "whTW" in response.url:
            channel = "台湾"
        elif "economic" in response.url:
            channel = "财经"
        elif "investmentandfinancial" in response.url:
            channel = "理财"
        elif "financialhotspot" in response.url:
            channel = "财经热点"
        elif "whphysicaleducation" in response.url:
            channel = "体育"
        elif "whentertainment" in response.url:
            channel = "娱乐"
        a_tags = response.css('a')
        # 遍历每个 <a> 标签，获取链接和文本
        for a_tag in a_tags:
            try:
                link = a_tag.attrib['href']
            except Exception as e:
                continue
            self.logger.debug(f"link:{link}")
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True,
                                 meta={"channel":channel, "source": self.source})

    def parse_page(self, response):
        yield parse_detail(response, self.crawler.redis_client)
