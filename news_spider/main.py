from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

crawler = CrawlerProcess(settings)

# crawler.crawl('news_hunan')  # 湖南在线
# crawler.crawl('news_m4')  # 四月
# crawler.crawl('newssc')  # 四川新闻
# crawler.crawl('dayoo')  # 广州日报大洋网
# crawler.crawl('gmw')  # 光明网
# crawler.crawl('scol')  # 四川在线
# crawler.crawl('fjsen')  # 东南网
# crawler.crawl('cyol')  # 中青在线
# crawler.crawl('crntt')  # 中评网
# crawler.crawl('takefoto')  # 北晚在线

crawler.crawl('ccn')  # 中国消费网



# crawler.start()
crawler.start()