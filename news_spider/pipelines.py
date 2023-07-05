# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import time

import logging

from warehouse import models


class NewsSpiderPipeline:
    def __init__(self):
        self.start_time = None
        self.logger = logging.getLogger(__name__)
        self.count = 0
        self.item_list = []

    def open_spider(self, spider):
        self.start_time = time.time()

    def process_item(self, item, spider):
        if item:
            # item.save()
            # spider.crawler.redis_client.sadd('urls', item["url"])
            self.item_list.append(item)
            self.logger.debug(f"保存：{item['source']}:{item['title']}- {item['url']}")
            self.count += 1
            # self.logger.info(f"{item['source']}-> 长度{len(self.item_list)}, 第一条:{self.item_list[0]}")
            # print(f"保存：{item['title']}")
            # 一千条数据存储一次
            if len(self.item_list) >= 1000:
                self.save_item()

        return item

    def save_item(self):
        # 将BookItem对象转换为Book模型对象
        news_to_create = [
            models.News(title=item["title"], url=item["url"], content=item["content"], images=item["images"],
                        channel=item["channel"], source=item["source"], publish_time=item["publish_time"])
            for item in self.item_list
        ]

        # 手动为每个对象分配主键
        for book in news_to_create:
            book.pk = None
        # 统一创建
        models.News.objects.bulk_create(news_to_create)
        self.item_list = []

    def close_spider(self, spider):
        # 在爬虫关闭时执行的操作
        # 可以进行清理工作，例如关闭文件、断开数据库连接等
        # 获取程序结束时间
        self.save_item()

        end_time = time.time()

        # 计算耗时（秒）
        elapsed_time = end_time - self.start_time

        # 将耗时转换为时分秒格式
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)

        # 打印耗时情况
        self.logger.info(f"共新增数据：{self.count}条。")
        self.logger.warning("程序运行耗时：{}时{}分{}秒".format(hours, minutes, seconds))


