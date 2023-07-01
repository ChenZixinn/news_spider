# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from warehouse.models import News
from scrapy_djangoitem import DjangoItem


class NewsSpiderItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model = News




