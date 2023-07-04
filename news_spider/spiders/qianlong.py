import scrapy

from news_spider.utils.page_util import parse_detail


class QianlongSpider(scrapy.Spider):
    name = 'qianlong'
    source = "千龙网"
    allowed_domains = ['qianlong.com']
    start_urls = []
    for i in range(1, 101):
        start_urls.append(f"https://china.qianlong.com/{i}.shtml")
        start_urls.append(f'https://beijing.qianlong.com/{i}.shtml')
        start_urls.append(f'https://world.qianlong.com/{i}.shtml')
        start_urls.append(f'https://dangjian.qianlong.com/{i}.shtml')
        start_urls.append(f'https://review.qianlong.com/{i}.shtml')
        start_urls.append(f'https://finance.qianlong.com/{i}.shtml')
        start_urls.append(f'https://tech.qianlong.com/{i}.shtml')
        start_urls.append(f'https://culture.qianlong.com/{i}.shtml')
        start_urls.append(f'https://edu.qianlong.com/{i}.shtml')
        start_urls.append(f'https://sports.qianlong.com/{i}.shtml')

    def parse(self, response):
        a_elements = response.xpath("//div[contains(@class, 's_pc_rdjx_box')]//a")
        self.logger.debug(f"a_elements.len{len(a_elements)}")
        for a in a_elements:
            # 处理匹配到的 <a> 元素
            link = a.attrib.get('href')
            self.logger.debug(f"link:{link}")
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True)

    def parse_page(self, response):
        channel = response.xpath("//div[contains(@class, 'mbx')]//a/text()").extract_first()
        response.meta["source"] = self.source
        response.meta["channel"] = channel
        # self.logger.debug(f"频道：{channel}")
        yield parse_detail(response, self.crawler.redis_client)
