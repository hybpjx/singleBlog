# Generated by Django 3.2.8 on 2021-10-21 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20211021_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='is_hot',
            field=models.BooleanField(default=0, verbose_name='是否成为热门'),
        ),
    ]