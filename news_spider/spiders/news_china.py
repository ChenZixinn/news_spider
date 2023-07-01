import scrapy

from news_spider.utils.page_util import check_link, parse_detail


class NewChinaSpider(scrapy.Spider):
    name = 'news_china'
    source = "中华网"
    allowed_domains = ['news.china.com', 'sports.china.com']
    start_urls = ['http://news.china.com/',
                  "https://news.china.com/international/index.html",
                  "https://news.china.com/social/index.html",
                  "https://sports.china.com/",
                  "https://military.china.com/",
                  "https://finance.china.com/",
                  "https://news.china.com/news100/",
                  "https://news.china.com/zw/",
                  "https://news.china.com/beijing2022/"]

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
            exclude = ['index', 'general', 'licence']
            include = ["html"]
            if not check_link(link, include, exclude):
                continue
            # print(link)
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True)

    def parse_page(self, response):
        channel = response.xpath('//div[@id="chan_breadcrumbs"]/a[1]/text()').extract_first()
        if not channel:
            if "social" in response.url:
                channel = "社会"
            elif "military" in response.url:
                channel = "军事"
            elif 'ent' in response.url:
                channel = "娱乐"
            elif 'finance' in response.url:
                channel = "财经"
            else:
                self.logger.warning(f"没找到频道：{response.url}")
        response.meta["source"] = self.source
        response.meta["channel"] = channel
        # self.logger.debug(f"频道：{channel}, url: {response.url}")
        yield parse_detail(response)

