import scrapy

from news_spider.utils.page_util import check_link, parse_detail


class ScolSpider(scrapy.Spider):
    name = 'scol'
    allowed_domains = ['ent.scol.com.cn']
    source = "四川在线"
    start_urls = ['https://ent.scol.com.cn/ylgg/index.html',"https://focus.scol.com.cn/gcdt/index.html",
                  "https://focus.scol.com.cn/zgsz/index.html", "https://focus.scol.com.cn/gjyw/index.html",
                  "https://focus.scol.com.cn/shwx/index.html", "https://focus.scol.com.cn/gjyw/index.html", ]
    for i in range(2,32):
        start_urls.append(f"https://ent.scol.com.cn/ylgg/index_{i}.html")
    for i in range(2, 51):
        start_urls.append(f"https://focus.scol.com.cn/gcdt/index_{i}.html")
        start_urls.append(f"https://focus.scol.com.cn/zgsz/index_{i}.html")
        start_urls.append(f"https://focus.scol.com.cn/gjyw/index_{i}.html")
        start_urls.append(f"https://focus.scol.com.cn/shwx/index_{i}.html")


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

            # exclude = ['mail', 'index', 'about', 'node']
            # include = ['htm', "http", "gmw"]
            if link.startswith("//"):
                link = "https:" + link
            exclude = []
            include = ["http", "html"]
            if not check_link(link, include, exclude):
                continue

            # print(link)
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True)

    def parse_page(self, response):
        channel = response.xpath('//*[@id="page_head"]/ul/li[2]/a[1]/text()').extract_first()
        response.meta["source"] = self.source
        response.meta["channel"] = channel
        yield parse_detail(response, self.crawler.redis_client)