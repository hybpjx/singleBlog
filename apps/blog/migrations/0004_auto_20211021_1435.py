# Generated by Django 3.2.8 on 2021-10-21 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_sidebar'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_hot',
            field=models.BooleanField(default=0, verbose_name='浏览量'),
        ),
        migrations.AddField(
            model_name='article',
            name='pageview',
            field=models.IntegerField(default=0, verbose_name='浏览量'),
        ),
    ]