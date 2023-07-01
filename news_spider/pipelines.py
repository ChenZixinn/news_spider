# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import time

import logging


class NewsSpiderPipeline:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.count = 0
        self.start_time = time.time()

    def process_item(self, item, spider):
        if item:
            item.save()
            print(f"保存：{item['source']}:{item['title']}")
            self.logger.info(f"保存：{item['source']}:{item['title']}- {item['url']}")
            self.count += 1
            # print(f"保存：{item['title']}")
        return item

    def close_spider(self, spider):
        # 在爬虫关闭时执行的操作
        # 可以进行清理工作，例如关闭文件、断开数据库连接等
        # 获取程序结束时间
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


