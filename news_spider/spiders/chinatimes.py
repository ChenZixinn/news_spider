import scrapy

from news_spider.utils.page_util import parse_detail


class ChinatimesSpider(scrapy.Spider):
    name = 'chinatimes'
    source = "华夏时报网"
    allowed_domains = ['chinatimes.net.cn']
    start_urls = []
    for i in range(1,51):
        start_urls.append(f'https://www.chinatimes.net.cn/finance/yaowen?page={i}')
        start_urls.append(f'https://www.chinatimes.net.cn/finance/diaocha?page={i}')
        start_urls.append(f'https://www.chinatimes.net.cn/finance/zhengce?page={i}')
        start_urls.append(f'https://www.chinatimes.net.cn/category/quyu?page={i}')
        start_urls.append(f'https://www.chinatimes.net.cn/finance/zhengquan?page={i}')
        start_urls.append(f'https://www.chinatimes.net.cn/finance/jinrong?page={i}')
        start_urls.append(f'https://www.chinatimes.net.cn/finance/gongsi?page={i}')
        start_urls.append(f'https://www.chinatimes.net.cn/finance/jiankang?page={i}')
        start_urls.append(f'https://www.chinatimes.net.cn/finance/dichan?page={i}')
        start_urls.append(f'https://www.chinatimes.net.cn/finance/qiche?page={i}')
        start_urls.append(f'https://www.chinatimes.net.cn/finance/nengyuan?page={i}')

    def parse(self, response):
        divs = response.xpath("//div[contains(@class, 'list_news')]/div")
        for div in divs:
            link = div.xpath('.//a[1]/@href').get()
            if link:
                link = "https://www.chinatimes.net.cn" + link
                yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True)

    def parse_page(self, response):
        channel = response.xpath("//div[contains(@class, 'contentpart')]/p/a[last()]/text()").extract_first()
        response.meta["source"] = self.source
        response.meta["channel"] = channel
        if not channel:
            self.logger.error(f"频道找不到:{channel}, url: {response.url}")
        yield parse_detail(response, self.crawler.redis_client)
