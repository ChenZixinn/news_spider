import scrapy

from news_spider.utils.page_util import check_link, parse_detail


class CeSpider(scrapy.Spider):
    name = 'ce'
    source = "中国经济网"
    allowed_domains = ['ce.cn', 'intl.ce.cn']
    # sp=食品 shgj=社会国际  kj=科技 more=宏观经济 fazhi=法制 quanqiu=全球时事 guoji/jingji=国际经济
    start_urls = ['http://www.ce.cn/cysc/sp/zhongjingyuqing/index.shtml',
                  'http://www.ce.cn/cysc/sp/yishiting/',
                  "http://www.ce.cn/xwzx/shgj/gdxw/index.shtml",
                  "http://www.ce.cn/xwzx/kj/index.shtml",
                  "http://www.ce.cn/macro/more/index.shtml",
                  "http://www.ce.cn/xwzx/fazhi/index.shtml",
                  "http://intl.ce.cn/guoji/quanqiu/index.shtml",
                  "http://intl.ce.cn/guoji/jingji/"
                  ]
    for i in range(1,34):
        start_urls.append(f'http://www.ce.cn/cysc/sp/zhongjingyuqing/index._{i}shtml',)
        start_urls.append(f'http://www.ce.cn/cysc/sp/yishiting/index._{i}shtml',)
        start_urls.append(f"http://www.ce.cn/xwzx/shgj/gdxw/index._{i}shtml",)
        start_urls.append(f"http://www.ce.cn/xwzx/kj/index._{i}shtml",)
        start_urls.append(f"http://www.ce.cn/macro/more/index._{i}shtml",)
        start_urls.append(f"http://www.ce.cn/xwzx/fazhi/index._{i}shtml",)
        start_urls.append(f"http://intl.ce.cn/guoji/quanqiu/index._{i}shtml",)
        start_urls.append(f"http://intl.ce.cn/guoji/jingji/index_{i}.shtml")

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
            exclude = ["index"]
            include = ["shtml"]
            if not check_link(link, include, exclude):
                continue

            # 相对路径的转换
            if "../../" in link:
                link = response.url[:response.url[:response.url[:response.url.rfind("/")].rfind("/")].rfind("/")] + link.replace("../../", "/")
            elif "../" in link:
                link = response.url[:response.url[:response.url.rfind("/")].rfind("/")] + link.replace("../", "/")
            elif link.startswith("./"):
                end_index = response.url.rfind("/")
                link = response.url[0:end_index] + link.replace("./", "/")
            # print(f"{link}, parent:{response.url}")
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True)

    def parse_page(self, response):
        channel = response.xpath('(//a[contains(@class, "CurrChnlCls")])[last()]/text()').extract_first()
        response.meta["source"] = self.source
        response.meta["channel"] = channel
        # self.logger.debug(f"频道：{channel}")
        yield parse_detail(response, self.crawler.redis_client)
