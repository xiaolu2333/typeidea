# Generated by Django 3.1.7 on 2021-09-22 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_auto_20210923_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='target',
            field=models.URLField(max_length=100, verbose_name='评论目标'),
        ),
    ]
