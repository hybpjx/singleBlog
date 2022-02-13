# Generated by Django 3.2.10 on 2022-02-12 21:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0016_alter_emailverifycode_send_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifycode',
            name='send_type',
            field=models.CharField(choices=[('forget', '找回密码'), ('register', '注册')], default='register', max_length=16, verbose_name='验证种类'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='owner',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]