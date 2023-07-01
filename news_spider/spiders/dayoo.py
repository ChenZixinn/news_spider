import scrapy

from news_spider.utils.page_util import parse_detail, check_link


class DayooSpider(scrapy.Spider):
    name = 'dayoo'
    source = "广州日报大洋网"
    allowed_domains = ['dayoo.com']
    # 首页 文化 热闻 热评 新活广州
    start_urls = ['https://www.dayoo.com/', 'https://news.dayoo.com/culture/159140.shtml',
                  "https://news.dayoo.com/guangzhou/150955.shtml", "https://news.dayoo.com/guangzhou/153828.shtml",
                  'https://news.dayoo.com/NewGZ/159135.shtml', "https://news.dayoo.com/kechuang/155401.shtml"]
    for i in range(2, 6):
        start_urls.append(f"https://news.dayoo.com/culture/159140_{i}.shtml")
        start_urls.append(f"https://news.dayoo.com/guangzhou/150955_{i}.shtml")
        start_urls.append(f"https://news.dayoo.com/guangzhou/153828_{i}.shtml")
        start_urls.append(f"https://news.dayoo.com/NewGZ/159135_{i}.shtml")
        start_urls.append(f"https://news.dayoo.com/kechuang/155401_{i}.shtml")

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
            exclude = ['node', 'portal', 'html', 'shtml', 'index']
            include = ['htm']
            if not check_link(link, include, exclude):
                continue
            # print(link)
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True)

    def parse_page(self, response):
        channel = response.xpath('//div[@class="crumbs"]/a[last()]/text()').extract_first()
        response.meta["source"] = self.source
        response.meta["channel"] = channel

        yield parse_detail(response)