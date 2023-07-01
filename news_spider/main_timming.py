import time

import schedule
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def run_crawler():
    settings = get_project_settings()

    crawler = CrawlerProcess(settings)

    crawler.crawl('news_hunan')  # 湖南在线
    crawler.crawl('news_m4')  # 四月
    crawler.crawl('newssc')  # 四川新闻
    crawler.crawl('dayoo')  # 广州日报大洋网
    crawler.crawl('gmw')  # 光明网

    crawler.crawl('scol')  # 四川在线
    crawler.crawl('fjsen')  # 东南网
    crawler.crawl('cyol')  # 中青在线
    crawler.crawl('crntt')  # 中评网
    crawler.crawl('takefoto')  # 北晚在线

    crawler.crawl('ccn')  # 中国消费网
    crawler.crawl('stdaily')  # 中国科技网
    crawler.crawl('ce')  # 中国经济网
    crawler.crawl('chinadaily')  # 中国日报
    crawler.crawl('zgjtb')  # 中国交通新闻网

    crawler.crawl('cet')  # 中国经济新闻网
    crawler.crawl('news_china')  # 中华网
    crawler.crawl('wenming')  # 文明网
    crawler.crawl('southcn')  # 南方网
    crawler.crawl('chinanews')  # 中国新闻网

    # crawler.start()
    crawler.start()

# 使用schedule库来调度任务，在每天的2点执行run_crawler函数
schedule.every().day.at("02:00").do(run_crawler)


if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)