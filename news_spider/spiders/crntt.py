import scrapy

from news_spider.utils.page_util import check_link, parse_detail


class CrnttSpider(scrapy.Spider):
    name = 'crntt'
    source = "中评网"
    allowed_domains = ['crntt.com']
    start_urls = []
    for i in range(1, 51):
        # 经济
        start_urls.append(f"http://www.crntt.com/crn-webapp/oneOutline.jsp?coluid=50&page={i}")
        # 中国领导人
        start_urls.append(f"http://www.crntt.com/crn-webapp/msgOutline.jsp?coluid=357&page={i}")
        # 大陆新闻
        start_urls.append(f"http://www.crntt.com/crn-webapp/msgOutline.jsp?page={i}&coluid=45")
        # 智库汇聚
        start_urls.append(f"http://www.crntt.com/crn-webapp/msgOutline.jsp?page={i}&coluid=266")
        # 经济
        start_urls.append(f"http://www.crntt.com/crn-webapp/msgOutline.jsp?page={i}&coluid=253")
        # 国内财经
        start_urls.append(f"http://www.crntt.com/crn-webapp/kindOutline.jsp?coluid=10&kindid=253&page={i}")
        # 国际财经
        start_urls.append(f"http://www.crntt.com/crn-webapp/kindOutline.jsp?coluid=10&kindid=254&page={i}")


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
            include = ["doc"]
            if not check_link(link, include, exclude):
                continue
            if link.startswith("."):
                link = "http://www.crntt.com/crn-webapp" + link[1:]

            else:
                link = "http://www.crntt.com" + link
            # print(link)
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True)

    def parse_page(self, response):
        # channel = response.xpath('/html/body/div[2]/table[4]/tbody/tr/td/table[1]/tbody/tr[1]/td[1]/a[2]/text()').extract_first()
        if "coluid=357" in response.url:
            channel = "中国领导人"
        elif "coluid=50" in response.url:
            channel = "经济"
        elif "coluid=45" in response.url:
            channel = "大陆新闻"
        elif "coluid=266" in response.url:
            channel = "智库汇聚"
        elif "coluid=253" in response.url:
            channel = "经济"
        elif "coluid=10" in response.url and "kindid=253":
            channel = "国内财经"
        elif "coluid=10" in response.url and "kindid=254":
            channel = "国际财经"
        else:
            channel = "首页"
        response.meta["source"] = self.source
        response.meta["channel"] = channel
        # self.logger.debug(f"频道：{channel}")
        yield parse_detail(response)
