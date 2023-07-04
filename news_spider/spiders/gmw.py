import scrapy

from news_spider.utils.page_util import parse_detail

from news_spider.utils.page_util import check_link


class GmwSpider(scrapy.Spider):
    name = 'gmw'
    source = "中国文明网"
    allowed_domains = ['www.gmw.cn', 'gmw.cn', 'world.gmw.cn', 'life.gmw.cn', 'tech.gmw.cn', 'economy.gmw.cn', "culture.gmw.cn"]
    # 首页 国际 生活 科技 经济
    start_urls = ['https://www.gmw.cn/', "https://world.gmw.cn/node_4485.htm", "https://life.gmw.cn/node_9268.htm",
                  "https://tech.gmw.cn/node_10249.htm", "https://economy.gmw.cn/node_8971.htm",
                  "https://culture.gmw.cn/node_10570.htm", "https://jiankang.gmw.cn/node_12215.htm",
                  "https://sports.gmw.cn/node_9638.htm", "https://politics.gmw.cn/node_26858.htm"]
    for i in range(2, 11):
        start_urls.append(f"https://world.gmw.cn/node_4485_{i}.htm")
        start_urls.append(f"https://life.gmw.cn/node_9268_{i}.htm")
        start_urls.append(f"https://tech.gmw.cn/node_10249_{i}.htm")
        start_urls.append(f"https://economy.gmw.cn/node_8971_{i}.htm")
        start_urls.append(f"https://culture.gmw.cn/node_10570_{i}.htm")
        start_urls.append(f"https://politics.gmw.cn/node_26858_{i}.htm")
    for i in range(2, 6):
        start_urls.append(f"https://jiankang.gmw.cn/node_12215_{i}.htm")
        start_urls.append(f"https://sports.gmw.cn/node_9638_{i}.htm")


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
            exclude = ['mail','index','about','node']
            include = ['htm', "http", "gmw"]
            if not check_link(link, include, exclude):
                continue

            # print(link)
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True)

    def parse_page(self, response):
        # channel = response.xpath('/html/body/div[5]/div[1]/div[1]/a[position() = last() - 1]/text()').extract_first()
        channel = response.xpath('/html/body/div[5]/a[3]/text()').extract_first()
        response.meta["source"] = self.source
        response.meta["channel"] = channel
        yield parse_detail(response, self.crawler.redis_client)
