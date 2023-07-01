import scrapy

from news_spider.utils.page_util import check_link, parse_detail


class CetSpider(scrapy.Spider):
    name = 'cet'
    source = "中国经济新闻网"
    allowed_domains = ['cet.com.cn']
    start_urls = ["https://www.cet.com.cn/",
                  'https://www.cet.com.cn/wzsy/ycxw/index.shtml',
                  "https://www.cet.com.cn/itpd/index.shtml"
                  "https://www.cet.com.cn/wzsy/df/index.shtml",
                  "https://www.cet.com.cn/wzsy/jdxw/index.shtml"]
    for i in range(2, 51):
        start_urls.append(f"https://www.cet.com.cn/wzsy/ycxw/index_{i}.shtml")
        start_urls.append(f"https://www.cet.com.cn/wzsy/df/index_{i}.shtml")
        start_urls.append(f"https://www.cet.com.cn/wzsy/jdxw/index_{i}.shtml")

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
            exclude = ['index']
            include = ["shtml"]
            if not check_link(link, include, exclude):
                continue
            link = "https://www.cet.com.cn" + link
            # print(link)
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True)

    def parse_page(self, response):
        channel = response.xpath('//div[contains(@class, "threeContentHeader")]/p[1]/a[2]/text()').extract_first()
        response.meta["source"] = self.source
        response.meta["channel"] = channel
        # self.logger.debug(f"频道：{channel}, url: {response.url}")
        yield parse_detail(response)
