# Generated by Django 3.1.7 on 2021-09-22 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_auto_20210505_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(max_length=2000, verbose_name='内容'),
        ),
    ]