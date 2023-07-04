import scrapy

from news_spider.utils.page_util import check_link, parse_detail


class ZgjtbSpider(scrapy.Spider):
    name = 'zgjtb'
    source = "中国交通新闻网"
    allowed_domains = ['zgjtb.com']
    start_urls = ['https://www.zgjtb.com/node_141_2.html',
                  "https://www.zgjtb.com/node_15626.html",
                  "https://www.zgjtb.com/node_15627.html",
                  "https://www.zgjtb.com/node_15628.html",
                  "https://www.zgjtb.com/node_15630.html",
                  "https://www.zgjtb.com/node_15492.html",
                  "https://www.zgjtb.com/node_15493.html",
                  "https://www.zgjtb.com/node_1022.html",
                  "https://www.zgjtb.com/node_146.html",
                  "https://www.zgjtb.com/node_15491.html",
                  "https://www.zgjtb.com/node_10005.html",
                  "https://www.zgjtb.com/node_10074.html",
                  "https://www.zgjtb.com/zhitong/node_380.html",
                  "https://www.zgjtb.com/index.html"
                  ]
    for i in range(2,11):
        start_urls.append(f"https://www.zgjtb.com/node_141_{i}.html")
        start_urls.append(f"https://www.zgjtb.com/node_1022_{i}.html")
        start_urls.append(f"https://www.zgjtb.com/node_146_{i}.html")
        start_urls.append(f"https://www.zgjtb.com/node_15491_{i}.html")
        start_urls.append(f"https://www.zgjtb.com/node_10005_{i}.html")
        start_urls.append(f"https://www.zgjtb.com/node_380_{i}.html")

    def parse(self, response):
        """获取页面所有链接，并进入提取内容"""
        a_tags = response.css('a')
        # 遍历每个 <a> 标签，获取链接和文本
        for a_tag in a_tags:
            try:
                link = a_tag.attrib['href']
            except Exception as e:
                continue
            # 不存在返回
            if link.startswith("//"):
                link = "https:" + link
            exclude = []
            include = ["content"]
            if not check_link(link, include, exclude):
                continue
            # print(link)
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True)

    def parse_page(self, response):
        channel = response.xpath('//div[contains(@class, "current")]/span[1]/a[last()]/text()').extract_first()
        response.meta["source"] = self.source
        response.meta["channel"] = channel
        yield parse_detail(response, self.crawler.redis_client)
