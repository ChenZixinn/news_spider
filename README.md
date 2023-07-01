### 项目介绍
项目基于Scrapy实现，爬取新闻网站主要新闻，通过gen库提取内容，存储到mysql中。实现定时爬取和增量爬取。

##### 已爬取：

- 湖南在线
- 四月
- 四川新闻
- 广州日报大洋网
- 光明网
- 四川在线
- 东南网
- 中青在线
- 中评网
- 北晚在线



### 项目部署

数据模型通过Django ORM模型完成，使用前需要**导入数据库**或者**初始化**



##### 数据库设置

/news_web/settings.py

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
        "NAME": "数据库名",
        "USER": "用户",
        "PASSWORD": "密码",
        "HOST": "ip",
        "POST": 3306
    }
}
```



##### 导入数据库

```shell
source ./data_bak.sql
```



##### 初始化

```shell
python manage.py makemigrations
python manage.py migrate
```



### 项目运行

##### 直接运行

```shell
cd news_spider/
python main.py
```



##### 定时爬取

```shell
TODO
```



