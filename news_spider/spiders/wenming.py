import scrapy

from news_spider.utils.page_util import check_link, parse_detail


class WenmingSpider(scrapy.Spider):
    name = 'wenming'
    source = "中国文明网"
    allowed_domains = ['wenming.cn']
    start_urls = ['http://wenming.cn/', "http://www.wenming.cn/ttn/zyjh/index.shtml",
                  "http://www.wenming.cn/y22/index.shtml", "http://www.wenming.cn/bbgz/gzjj/index.shtml",
                  "http://www.wenming.cn/bbgz/ywdt/", "http://www.wenming.cn/cy/"]
    for i in range(2, 6):
        start_urls.append(f"http://www.wenming.cn/ttn/zyjh/index_{i}.shtml")
        start_urls.append(f"http://www.wenming.cn/y22/index_{i}.shtml")
        start_urls.append(f"http://www.wenming.cn/bbgz/gzjj/index_{i}.shtml")
        start_urls.append(f"http://www.wenming.cn/bbgz/ywdt/index_{i}.shtml")

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
            exclude = ['index']
            include = ["shtml"]
            if not check_link(link, include, exclude):
                continue
            if "../../" in link:
                link = response.url[
                       :response.url[:response.url[:response.url.rfind("/")].rfind("/")].rfind("/")] + link.replace(
                    "../../", "/")
            elif "../" in link:
                link = response.url[:response.url[:response.url.rfind("/")].rfind("/")] + link.replace("../", "/")
            elif link.startswith("./"):
                end_index = response.url.rfind("/")
                link = response.url[0:end_index] + link.replace("./", "/")
            # print(link)
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True, meta={"parent": link})

    def parse_page(self, response):
        channel = response.xpath('(//a[contains(@class, "CurrChnlCls")])[2]/text()').extract_first()
        if not channel:
            channel = "首页"
            self.logger.warning(f"找不到频道：{response.url}, parent = {response.meta['parent']}")
        response.meta["source"] = self.source
        response.meta["channel"] = channel
        # self.logger.debug(f"频道：{channel}, url: {response.url}")
        yield parse_detail(response)
