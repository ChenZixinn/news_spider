import scrapy

from news_spider.utils.page_util import parse_detail


class ZjolSpider(scrapy.Spider):
    name = 'zjol'
    source = "浙江在线"
    allowed_domains = ['zjol.com.cn']
    start_urls = ['https://china.zjol.com.cn/', 'https://zjnews.zjol.com.cn/yc/',
                  'https://opinion.zjol.com.cn/cp/sptt/index.shtml']
    for i in range(1, 29):
        start_urls.append(f"https://opinion.zjol.com.cn/cp/sptt/index_{i}.shtml")
    # start_urls = ['https://zjnews.zjol.com.cn/yc/']

    def parse(self, response):
        # 获取ul下所有的li>a标签
        links = response.xpath('//ul[contains(@class, "newslist")]/li/a/@href').getall()
        if not links:
            links = response.xpath('//ul[contains(@id, "Ullist")]/li/a/@href').getall()
        for link in links:
            if link.startswith("//"):
                link = "https:" + link
                # self.logger.debug(f"link:{link}")
                yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True)


    def parse_page(self, response):
        channel = response.xpath("(//a[contains(@class, 'CurrChnlCls')])[last()]/text()").extract_first()
        response.meta["source"] = self.source
        response.meta["channel"] = channel
        # self.logger.debug(f"频道为:{channel}")
        yield parse_detail(response, self.crawler.redis_client)
