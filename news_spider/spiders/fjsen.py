import scrapy

from news_spider.utils.page_util import parse_detail, check_link


class FjsenSpider(scrapy.Spider):
    name = 'fjsen'
    source = "东南网"
    allowed_domains = ['fjsen.com']
    # 教育咨询
    start_urls = ['http://www.fjsen.com/node_305144.htm', "http://www.fjsen.com/node_177420.htm",
                  "http://news.fjsen.com/C_Society.htm", "http://news.fjsen.com/WorldSociety.htm"]
    for i in range(2, 11):
        start_urls.append(f"http://www.fjsen.com/node_305144_{i}.htm")
        start_urls.append(f"http://www.fjsen.com/node_177420_{i}.htm")
        start_urls.append(f"http://news.fjsen.com/C_Society_{i}.htm")
        start_urls.append(f"http://news.fjsen.com/WorldSociety_{i}.htm")

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

            # exclude = ["index", "about","map", "china", "view", "gov", "introduce", "yc","rss", "C_Society", "WorldSociety","zhuanti","nodee"]
            exclude = ['/tv']
            include = ["http", "htm", "content"]
            if not check_link(link, include, exclude):
                continue
            # print(link)
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True)

    def parse_page(self, response):
        channel = response.xpath('//a[contains(@class, "daohang")][1]/text()').extract_first()
        if "_" in channel:
            channel.replace("_", "")
        response.meta["source"] = self.source
        response.meta["channel"] = channel
        yield parse_detail(response, self.crawler.redis_client)
