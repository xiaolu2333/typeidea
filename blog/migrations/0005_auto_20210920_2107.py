# Generated by Django 3.1.7 on 2021-09-20 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_is_md'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='is_md',
            field=models.BooleanField(default=False, help_text='选择文档语法：', verbose_name='markdown吾法'),
        ),
    ]
