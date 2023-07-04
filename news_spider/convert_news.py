from datetime import datetime
import os
import django
# 设置环境变量 DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_web.settings")
# 加载 Django 的设置
django.setup()

from news_web import settings
from warehouse.models import News

import os
import datetime
from django.conf import settings
from pyltp import SentenceSplitter


def process_news_content():
    # 获取当前日期
    today = datetime.date.today().strftime("%Y%m%d")

    specified_date = datetime.date(2023, 7, 4)  # 替换为你要查询的日期

    # 获取所有的News对象
    # news_list = News.objects.filter()
    # 获取指定日期的News对象
    news_list = News.objects.filter(create_time__date=specified_date)

    # 分句并去除content中的内容
    sentences = []
    for news in news_list:
        content = news.content.replace("。】", "】").replace("。)", ")")

        # 使用分句模型进行中文句子分割
        sentences.extend(SentenceSplitter.split(content))
    # 去除多余的空行
    sentences = [sentence.strip() for sentence in sentences if sentence.strip() and len(sentence) > 4]

    # 将句子按每千条分割成文件
    num_sentences = len(sentences)
    chunk_size = 1000
    num_chunks = num_sentences // chunk_size + 1
    count = 1
    for i in range(num_chunks):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size
        chunk_sentences = sentences[start_idx:end_idx]

        # 将句子写入文件
        file_path = os.path.join(settings.BASE_DIR, f"data_txt/{today}_{count}.txt")

        while os.path.exists(file_path):
            count += 1
            file_path = os.path.join(settings.BASE_DIR, f"data_txt/{today}_{count}.txt")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write("\n".join(chunk_sentences))

        count += 1


if __name__ == "__main__":
    process_news_content()
