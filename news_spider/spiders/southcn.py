import scrapy

from news_spider.utils.page_util import check_link, parse_detail


class SouthcnSpider(scrapy.Spider):
    name = 'southcn'
    source = "南方网"
    allowed_domains = ['southcn.com']
    start_urls = ['https://www.southcn.com/']
    for i in range(1, 51):
        start_urls.append(f"https://news.southcn.com/node_179d29f1ce?cms_node_post_list_page={i}")
    for i in range(1, 11):
        start_urls.append(f"https://news.southcn.com/node_d16fadb650?cms_node_post_list_page={i}")

    def parse(self, response):
        """获取页面所有链接，并进入提取内容"""
        a_tags = response.css('a')
        # 遍历每个 <a> 标签，获取链接和文本
        for a_tag in a_tags:
            try:
                link = a_tag.attrib['href']
            except Exception as e:
                continue
            exclude = ["index"]
            include = ["shtml"]
            if not check_link(link, include, exclude):
                continue
            # print(link)
            channel = "首页"
            if "node_179d29f1ce" in response.url:
                channel = "热点"
            elif "node_d16fadb650" in response.url:
                channel = "最新动态"
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True, meta={"channel":channel})

    def parse_page(self, response):
        # channel = response.xpath("(//a[contains(@class, 'crm-link')])[1]/text()").extract_first()
        response.meta["source"] = self.source
        # response.meta["channel"] = channel
        # self.logger.debug(f"频道：{channel}, url: {response.url}")
        yield parse_detail(response)
