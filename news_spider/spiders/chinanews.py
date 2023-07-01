import scrapy

from news_spider.utils.page_util import check_link, parse_detail


class ChinanewsSpider(scrapy.Spider):
    name = 'chinanews'
    source = "中国新闻网"
    allowed_domains = ['chinanews.com']
    start_urls = ['https://www.chinanews.com.cn/scroll-news/news1.html',
                  "https://www.chinanews.com.cn/importnews.html",
                  "https://www.chinanews.com.cn/china.shtml",
                  "https://www.chinanews.com.cn/dxw.shtml",
                  "https://www.chinanews.com.cn/ll.shtml",
                  "https://www.chinanews.com.cn/world.shtml",
                  "https://www.chinanews.com.cn/society.shtml",
                  "https://www.chinanews.com.cn/cj/gd.shtml",
                  "https://www.chinanews.com.cn/dwq.shtml",
                  "https://www.chinanews.com.cn/huaren.shtml",
                  "https://www.chinanews.com.cn/wenhua.shtml",
                  "https://www.chinanews.com.cn/sports.shtml",
                  "https://www.chinanews.com.cn/life/gd.shtml",
                  "https://www.chinanews.com.cn/photo/more.shtml",
                  "https://www.chinanews.com.cn/best-news/news1.html"
                  ]

    def parse(self, response):
        """获取页面所有链接，并进入提取内容"""
        a_tags = response.css('a')
        # 遍历每个 <a> 标签，获取链接和文本
        for a_tag in a_tags:
            try:
                link = a_tag.attrib['href']
            except Exception as e:
                continue
            exclude = ["index", "shipin", "cl", "live.", "theory", '/u/', '/wine/',
                       "/dxw.shtml",
                       "/world.shtml",
                       "/society.shtml",
                       "/dwq.shtml",
                       "/huaren.shtml",
                       "/wenhua.shtml",
                       "/sports.shtml",
                       "/photo/more.shtml",
                       "/dxw.shtml",
                       "/world.shtml",
                       "/society.shtml",
                       "/dwq.shtml",
                       "/huaren.shtml",
                       "/wenhua.shtml",
                       "/sports.shtml",
                       "/photo/more.shtml",
                       "china.shtml",
                       "iframe","kong","footer","ll.shtml"
                       ]
            include = ["shtml"]
            if not check_link(link, include, exclude):
                continue
            if link.startswith("//"):
                link = "https:" + link
            elif link.startswith("/"):
                link = "https://www.chinanews.com.cn" + link
            channel = ""
            if "/gn/" in link:
                channel = "国内"
            elif "/dxw/" in link:
                channel = "东西问"
            elif "/ll/" in link:
                channel = "理论"
            elif "/gj/" in link:
                channel = "国际"
            elif "/sh/" in link:
                channel = "社会"
            elif "/cj/" in link:
                channel = "财经"
            elif "/dwq/" in link:
                channel = "大湾区"
            elif "/hr/" in link:
                channel = "华人"
            elif "/cul/" in link:
                channel = "文娱"
            elif "/ty/" in link:
                channel = "体育"
            elif "/life/" in link:
                channel = "健康·生活"
            elif "/tp/" in link:
                channel = "图片"
            else:
                self.logger.warning(f"没找到频道：{link}")

            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True,
                                 meta={"channel": channel})

    def parse_page(self, response):
        response.meta["source"] = self.source
        # self.logger.debug(f"频道：{response.meta['channel']}, url: {response.url}")
        yield parse_detail(response)
