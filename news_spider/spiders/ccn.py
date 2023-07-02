import scrapy

from news_spider.utils.page_util import check_link, parse_detail


class CcnSpider(scrapy.Spider):
    name = 'ccn'
    allowed_domains = ['ccn.com.cn']
    source = "中国消费网"
    # 要闻
    start_urls = ["https://www.ccn.com.cn/"]
    for i in range(1, 51):
        start_urls.append(f'https://www.ccn.com.cn/news/index.dhtml?page={i}')
        start_urls.append(f'https://www.ccn.com.cn/news/zonghe.dhtml?page={i}')
        start_urls.append(f'https://www.ccn.com.cn/news/hotnews.dhtml?page={i}')

    for i in range(1, 39):
        start_urls.append(f'https://www.ccn.com.cn/news/mainews.dhtml?page={i}')

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
            exclude = []
            include = ["Content"]
            if not check_link(link, include, exclude):
                continue

            if link.startswith("//"):
                link = "https:" + link
            else:
                link = "https://www.ccn.com.cn" + link
            # print(link)
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True)

    def parse_page(self, response):
        channel = response.xpath('/html/body/div[3]/div/div[5]/div/a[2]/text()').extract_first()
        response.meta["source"] = self.source
        response.meta["channel"] = channel
        # self.logger.debug(f"频道：{channel}")
        yield parse_detail(response)
