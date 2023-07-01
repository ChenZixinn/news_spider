import scrapy

from news_spider.utils.page_util import parse_detail, check_link


class ChinadailySpider(scrapy.Spider):
    name = 'chinadaily'
    source = "中国日报"
    allowed_domains = ['china.chinadaily.com.cn', 'chinadaily.com.cn']
    start_urls = [
                  ]

    for i in range(1,11):
        start_urls.append(f"https://china.chinadaily.com.cn/5bd5639ca3101a87ca8ff636/page_{i}.html")
        start_urls.append(f"http://china.chinadaily.com.cn/5bd5639ca3101a87ca8ff634/5bd5669ba3101a87ca8ff666/page_{i}.html")
        start_urls.append(f"http://world.chinadaily.com.cn/5bd55927a3101a87ca8ff618/page_{i}.html")
        start_urls.append(f"http://caijing.chinadaily.com.cn/5b7620c4a310030f813cf452/page_{i}.html")
        start_urls.append(f"http://tech.chinadaily.com.cn/5b7621d3a310030f813cf45b/page_{i}.html")
        start_urls.append(f"http://qiye.chinadaily.com.cn/5b7627bba310030f813cf47f/page_{i}.html")
        start_urls.append(f"http://caijing.chinadaily.com.cn/stock/5f646b7fa3101e7ce97253d3/page_{i}.html")
        start_urls.append(f"http://cn.chinadaily.com.cn/wenlv/5b7628dfa310030f813cf495/page_{i}.html")


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
            exclude = ['page', 'index']
            include = ["html"]
            if not check_link(link, include, exclude):
                continue
            # print(link)
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True, meta={"parent": response.url})

    def parse_page(self, response):
        # 检查重定向条件
        if response.meta.get('redirect_urls'):
            # 重定向发生
            self.logger.warning(f"发生了重定向，网站:{self.source},url:{response.meta['parent']}")
            return
        channel = response.xpath("(//div[contains(@class, 'da-bre')])[1]//a[last()]/text()").extract_first()
        if channel and " " in channel:
            channel = channel.split(" ")[-1]
        else:
            channel = "首页"
        response.meta["source"] = self.source
        response.meta["channel"] = channel
        # self.logger.debug(f"频道：{channel}, url: {response.url}, parent:{response.meta['parent']}")
        yield parse_detail(response)
