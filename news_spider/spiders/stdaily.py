import scrapy

from news_spider.utils.page_util import check_link, parse_detail


class StdailySpider(scrapy.Spider):
    name = 'stdaily'
    source = "中国科技网"
    allowed_domains = ['stdaily.com']
    start_urls = ['http://www.stdaily.com/index/kjxw/kjxw.shtml',
                  'http://www.stdaily.com/kjzc/top/common_list_2021_2.shtml',
                  "http://www.stdaily.com/kjzc/info/common_list_2021.shtml",
                  "http://www.stdaily.com/kjzc/focus/common_list_2021.shtml",
                  "http://www.stdaily.com/guoji/zongbian/zbjqd.shtml",
                  "http://www.stdaily.com/guoji/xinwen/kjxw.shtml",]
    for i in range(2,21):
        start_urls.append(f"http://www.stdaily.com/index/kjxw/kjxw_{i}.shtml")
        start_urls.append(f"http://www.stdaily.com/kjzc/top/common_list_2021_{i}.shtml")
        start_urls.append(f"http://www.stdaily.com/kjzc/info/common_list_2021_{i}.shtml")
        start_urls.append(f"http://www.stdaily.com/kjzc/focus/common_list_2021_{i}.shtml")
        start_urls.append(f"http://www.stdaily.com/guoji/zongbian/zbjqd_{i}.shtml")
        start_urls.append(f"http://www.stdaily.com/guoji/xinwen/kjxw_{i}.shtml")

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
            exclude = ['http', 'kjxw', 'index.', 'list', 'shentong', "kejixinwen.shtml"]
            include = ["shtml"]
            if not check_link(link, include, exclude):
                continue
            link = "http://www.stdaily.com" + link
            if "top" in response.url:
                channel = "最新报道"
            elif "focus" in response.url:
                channel = "要闻聚焦"
            elif "kjxw" in response.url:
                channel = "科技新闻"
            elif "info" in response.url:
                channel = "图解新闻"
            elif "zongbian" in response.url:
                channel = "总编辑圈点"
            elif "guoji/xinwen" in response.url:
                channel = "国际新闻"
            else:
                channel = "科技新闻"
            yield scrapy.Request(link, callback=self.parse_page, encoding="utf-8", dont_filter=True, meta={"channel": channel})

    def parse_page(self, response):
        response.meta["source"] = self.source
        yield parse_detail(response, self.crawler.redis_client)
