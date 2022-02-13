from django.db import models

# Create your models here.
from db.basemodel import BaseModel


class HelpSubmit(BaseModel):
    words = models.CharField(max_length=512, verbose_name='在线留言')

    class Meta:
        verbose_name = '留言板'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.words

class BugSubmit(BaseModel):
    name = models.CharField(max_length=16, verbose_name='用户姓名')
    email = models.EmailField(verbose_name='邮箱', blank=True, default='')
    bug = models.TextField(verbose_name='BUG提交')

    class Meta:
        verbose_name = 'bug汇总'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name + '提交的bug'
