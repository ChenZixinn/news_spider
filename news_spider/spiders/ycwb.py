import scrapy

from news_spider.utils.page_util import parse_detail


class YcwbSpider(scrapy.Spider):
    name = 'ycwb'
    source = "金羊网"
    allowed_domains = ['ycwb.com']
    start_urls = ['https://news.ycwb.com/n_bd_gz.htm',
                  "https://news.ycwb.com/n_gd_jd.htm",
                  "https://news.ycwb.com/n_gn_dt.htm",
                  "https://sp.ycwb.com/sp_1.htm",
                  "https://sp.ycwb.com/sp_2.htm",
                  "https://sp.ycwb.com/sp_6.htm",
                  "https://sp.ycwb.com/dsg.htm",
                  "https://news.ycwb.com/n_gj.htm"]
    for i in range(2,11):
        start_urls.append(f"https://news.ycwb.com/n_bd_gz_{i}.htm")
        start_urls.append(f"https://news.ycwb.com/n_gd_jd_{i}.htm")
        start_urls.append(f"https://news.ycwb.com/n_gn_dt_{i}.htm")
        start_urls.append(f"https://sp.ycwb.com/sp_1_{i}.htm")
        start_urls.append(f"https://sp.ycwb.com/sp_2_{i}.htm")
        start_urls.append(f"https://sp.ycwb.com/sp_6_{i}.htm")
        start_urls.append(f"https://sp.ycwb.com/dsg_{i}.htm")
        start_urls.append(f"https://news.ycwb.com/n_gj_{i}.htm")

    def parse(self, response):
        # class为lists的ul的li>a@href
        # 获取ul下所有的li>a标签
        links = response.xpath('//ul[contains(@class, "lists")]/li/a/@href').getall()
        if not links:
            links = response.xpath('//ul[contains(@class, "list_l")]/li/a/@href').getall()
        channel = ""
        if "bd_gz" in response.url:
            channel = "广州要闻"
        elif "gd_jd" in response.url:
            channel = "广东新闻"
        elif "gn_dt" in response.url:
            channel = "中国聚焦"
        elif "sp_1" in response.url:
            channel = "金羊视角"
        elif "sp_2" in response.url:
            channel = "媒体扫描"
        elif "sp_6" in response.url:
            channel = "广州观察"
        elif "n_gj" in response.url:
            channel = "国际"
        elif "dsg" in response.url:
            channel = "青年观察"
        for link in links:
            self.logger.debug(f"link:{link}")
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True,
                                 meta={"channel": channel, "source":self.source})

    def parse_page(self, response):
        yield parse_detail(response, self.crawler.redis_client)
