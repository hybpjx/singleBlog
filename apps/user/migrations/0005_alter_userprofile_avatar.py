# Generated by Django 3.2.8 on 2021-10-20 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20211019_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='images/default.jpg', upload_to='images/%Y/%m', verbose_name='用户头像'),
        ),
    ]
