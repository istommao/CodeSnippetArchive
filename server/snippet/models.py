"""snippet models"""
from django.db import models

from simditor.fields import RichTextField


class Snippet(models.Model):
    """Snippet."""

    title = models.CharField('标题', max_length=32)
    content = RichTextField()

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = 'Snippet'
        verbose_name_plural = 'Snippet'

    def __str__(self):
        return self.title
