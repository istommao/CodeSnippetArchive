"""snippet models"""
from django.db import models

from snippet import consts
from snippet.modelutils import PathAndRename


from simditor.fields import RichTextField


class Snippet(models.Model):
    """Snippet."""

    title = models.CharField('标题', max_length=32)
    intro = models.CharField('简介', max_length=256, default='')
    content = RichTextField()
    tags = models.CharField('标签', max_length=64, null=True, blank=True)

    image = models.ImageField(
        '图片', upload_to=PathAndRename('snippet/'),
        default=consts.DEFAULT_IMAGE
    )

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = 'Snippet'
        verbose_name_plural = 'Snippet'

    def __str__(self):
        return self.title

    @property
    def tag_list(self):
        tags = self.tags or ''
        tags = tags.strip('')
        if not tags:
            return []

        return tags.split(',')
