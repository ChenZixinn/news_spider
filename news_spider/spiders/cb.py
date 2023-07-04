import json
import time

import scrapy

from news_spider.utils.page_util import parse_detail


class CbSpider(scrapy.Spider):
    name = 'cb'
    source = "中国经营报"
    allowed_domains = ['cb.com.cn']
    start_urls = []

    def start_requests(self):
        # 自定义请求的URL列表
        url_video = "http://www.cb.com.cn/index/index/videoLoadMore"  # 深度
        url_index = "http://www.cb.com.cn/index/index/loadMoreEs"  # 首页
        url_general = "http://www.cb.com.cn/index/index/generalLoadMore"  # 要闻
        index_formdata = {
            "start": "1",
            "limit": "10"
        }
        video_formdata = {
            "start": '1',
            "limit": "12",
            "currentColumnId": "127"
        }
        general_formdata = {
            "limit": "10",
            "start": "1",
            "barId": "8",
            "per_id":""
        }
        for i in range(2, 200):
            yield scrapy.FormRequest(url=url_index,formdata=index_formdata,callback=self.parse_json)
            time.sleep(0.3)
            yield scrapy.FormRequest(url=url_video,formdata=video_formdata,callback=self.parse_json)
            time.sleep(0.3)
            yield scrapy.FormRequest(url=url_general,formdata=general_formdata,callback=self.parse_json)
            time.sleep(0.3)
            general_formdata["start"] = str(i)
            index_formdata["start"] = str(i)
            video_formdata["start"] = str(i)

    def parse_json(self, response):
        data = json.loads(response.text)
        data_list = data["data"].get("dataList")
        if not data_list:
            data_list = data["data"].get("newList")
        if data_list:
            for news in data_list:
                link = f'http://www.cb.com.cn{news["url"]}'

                self.logger.debug(f"link: {link}")
                yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True)

    def parse_page(self, response):
        channel = response.xpath("//ul[contains(@class, 'breadcrumbs')]/li[2]/a/text()").extract_first()
        response.meta["source"] = self.source
        response.meta["channel"] = channel
        self.logger.debug(f"频道:{channel}")
        yield parse_detail(response, self.crawler.redis_client)

