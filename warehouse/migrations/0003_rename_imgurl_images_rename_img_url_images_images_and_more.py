# Generated by Django 4.0.5 on 2023-06-29 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0002_remove_news_img_url_news_img_url'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ImgUrl',
            new_name='Images',
        ),
        migrations.RenameField(
            model_name='images',
            old_name='img_url',
            new_name='images',
        ),
        migrations.RenameField(
            model_name='news',
            old_name='img_url',
            new_name='images',
        ),
    ]
