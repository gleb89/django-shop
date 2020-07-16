from django.db import models


class Pages(models.Model):
    active = models.BooleanField('Активная', default=True, help_text='Опубликована ли страница?')
    title  = models.CharField('Заголовок страницы', max_length=255)
    slug   = models.SlugField('URL адрес страницы', max_length=100, unique=True)
    body   = models.TextField('Текст страницы', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
