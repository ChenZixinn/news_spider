import logging

from gne import GeneralNewsExtractor

from news_spider import items
from warehouse import models

logger = logging.getLogger(__name__)


def parse_detail(response):
    """
    传入页面的response，解析后返回items.news对象，response
    :param response: 页面请求结果，需要包含meta里的source来源和channel频道
    :return: item.news对象，请yield提交给管道
    """
    if not models.News.objects.filter(url=response.url).first():

        html = response.text
        if not html:
            return None
        extractor = GeneralNewsExtractor()
        try:
            result = extractor.extract(html)
        except Exception as e:
            logger.error(f'错误: {e}')
            return None
        news = items.NewsSpiderItem()
        news["title"] = result["title"]
        news["content"] = result["content"]
        news['url'] = response.url
        news['images'] = [img for img in result["images"] if "http" in img]
        news["channel"] = response.meta["channel"]
        news["source"] = response.meta["source"]
        news["publish_time"] = result["publish_time"]
        return news
    else:
        logger.debug(f"存在相同内容，跳过：{response.url}")
        # print(f"存在相同内容，跳过：{response.url}")


def check_link(link, include, exclude):
    """
    检查链接是否合法
    :param link: 链接
    :param include: 需要包含的字符串列表
    :param exclude: 不需要包含的字符串列表
    :return: True合法 False不合法
    """
    if not link:
        return False
    for i in include:
        if i not in link:
            return False

    for i in exclude:
        if i in link:
            return False
    return True