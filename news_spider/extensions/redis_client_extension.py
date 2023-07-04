import redis
from scrapy.utils import spider

from news_spider import settings


class RedisClientExtension:
    @classmethod
    def from_crawler(cls, crawler):
        host = settings.REDIS_HOST
        port = settings.REDIS_PORT
        password = settings.REDIS_PASSWORD
        db_index = settings.REDIS_DB_INDEX


        # 连接到Redis服务器
        redis_client = redis.Redis(host=host, port=port, db=db_index, password=password)

        # 在爬虫实例中注册Redis客户端
        crawler.redis_client = redis_client

        # 创建扩展实例
        ext = cls()

        # 将扩展实例返回给Scrapy引擎
        return ext
