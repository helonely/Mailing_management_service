from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(blank=True, max_length=200, null=True, verbose_name='slug'),
    content = models.TextField(verbose_name='содержимое'),
    picture = models.ImageField(upload_to='blog/', verbose_name='изображение', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='дата создания')
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'

