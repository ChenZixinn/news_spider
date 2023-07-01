import scrapy

from news_spider.utils.page_util import parse_detail, check_link


class CyolSpider(scrapy.Spider):
    name = 'cyol'
    source = "中青在线"
    allowed_domains = ['news.cyol.com']
    # 文化
    start_urls = ['http://news.cyol.com/gb/channels/J1VlJ8D7/index.html',
                  'http://news.cyol.com/gb/channels/vrbqX51Z/index.html',
                  "http://news.cyol.com/gb/channels/8Dgvq2rx/index.html",
                  "http://news.cyol.com/gb/channels/7ro4WZDy/index.html",
                  "http://news.cyol.com/gb/channels/VDWYLy1j/index.html",
                  "http://news.cyol.com/gb/channels/3DlVwd12/index.html",
                  "http://news.cyol.com/gb/channels/LkvjXQk7/index.html",
                  "http://news.cyol.com/gb/channels/3DjBMxD0/index.html",
                  "http://news.cyol.com/gb/channels/z1RJOo1q/index.html"]
    for i in range(2,51):
        start_urls.append(f'http://news.cyol.com/gb/channels/J1VlJ8D7/index_{i}.html')

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
            exclude = ["index"]
            include = ['html', "http", "content"]
            if not check_link(link, include, exclude):
                # self.logger.warning(f"url不符合要求：{link}")
                continue
            # print(link)
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True)

    def parse_page(self, response):
        channel = response.xpath("//div[contains(@class, 'pd')]/a[2]/text()").extract_first()
        response.meta["source"] = self.source
        response.meta["channel"] = channel
        yield parse_detail(response)

