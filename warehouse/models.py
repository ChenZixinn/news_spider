from django.db import models


class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    # images = models.ManyToManyField(Images)  # 图片，一对多
    images = models.TextField(blank=True, null=True)
    channel = models.CharField(max_length=32, blank=True, null=True)  # 频道
    source = models.CharField(max_length=32, blank=True, null=True)  # 来源
    publish_time = models.CharField(max_length=32, blank=True, null=True)  # 文章发布时间
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间，自动添加


