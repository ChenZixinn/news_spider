from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import sys
sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

from utils.init_redis import init_redis


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

    crawler.crawl('xinhua')  # 新华网
    crawler.crawl('eastday')  # 东方网
    crawler.crawl('wenweipo')  # 香港文汇网
    crawler.crawl('qianlong')  # 千龙网
    crawler.crawl('stnn')  # 星岛环球
    crawler.crawl("cb")  # 中国经营报
    crawler.crawl("zjol")  # 浙江在线
    crawler.crawl("ycwb")  # 金羊网
    crawler.crawl("gxnews")  # 广西新闻网
    crawler.crawl("chinatimes")  # 华夏时报网

    crawler.start()


if __name__ == "__main__":

    # init_redis()
    run_crawler()