# Generated by Django 4.0.4 on 2023-06-29 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='img_url',
        ),
        migrations.AddField(
            model_name='news',
            name='img_url',
            field=models.ManyToManyField(to='warehouse.imgurl'),
        ),
    ]
