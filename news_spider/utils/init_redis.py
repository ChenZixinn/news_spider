from datetime import datetime
import os
import django
# 设置环境变量 DJANGO_SETTINGS_MODULE
import redis
import os
import sys
sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])


from news_spider import settings



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_web.settings")
# 加载 Django 的设置
django.setup()

from warehouse.models import News


def init_redis(redis_client=None):
    if not redis_client:
        redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB_INDEX, password=settings.REDIS_PASSWORD)

    key = "urls"
    # 获取所有的News对象
    while redis_client.scard(key) > 0:
        redis_client.spop(key)

    news_list = News.objects.all()
    for news in news_list:
        if not redis_client.sismember('urls', news.url):
            redis_client.sadd('urls', news.url)
            # print(f'URL {news.url} added to Redis.')
        # else:
            # print(f'URL {news.url} already exists in Redis.')

if __name__ == '__main__':
    init_redis()