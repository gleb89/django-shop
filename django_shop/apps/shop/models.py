from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit


class Categories(models.Model):
    name = models.CharField('Название категории', max_length=255)
    slug = models.SlugField('URL категории', max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category:slug', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории товаров'


def main_image_upload_path(instance, filename):
    return f'products/{instance.sku}/{filename.lower()}'

class Products(models.Model):
    active         = models.BooleanField('Активный', default=True, help_text='Опубликован ли товар?')
    sku            = models.CharField('Артикул', max_length=50)
    name           = models.CharField('Название товара', max_length=255)
    categories     = models.ManyToManyField(Categories, verbose_name='Категории товара')
    price_discount = models.DecimalField('Цена без скидки', max_digits=8, decimal_places=2, blank=True, null=True)
    price          = models.DecimalField('Цена', max_digits=8, decimal_places=2)
    body           = models.TextField('Описание товара', blank=True, null=True)
    # main_image     = models.ImageField('Главное изображение', upload_to=main_image_upload_path, blank=True, null=True)
    main_image     = ProcessedImageField(verbose_name='Главное изображение',
                                        upload_to=main_image_upload_path,
                                        processors=[ResizeToFit(1920, 1080)],
                                        format='JPEG',
                                        options={'quality': 75},
                                        blank=True, null=True)

    main_image_thumbnail = ImageSpecField(source='main_image',
                                        # processors=[ResizeToFill(512, 512)],
                                        processors=[ResizeToFit(512, 512)],
                                        format='JPEG',
                                        options={'quality': 70})

    updated        = models.DateTimeField(auto_now=True, auto_now_add=False)

    # Thumbnail for admin
    def main_image_thumb(self):
        return mark_safe(f'<img style="width: 512px; height: auto;" src="{self.main_image.url}" alt="">')
    main_image_thumb.short_description = 'Главное изображение (thumb)'
    # END Thumbnail for admin

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


def product_image_upload_path(instance, filename):
    return f'products/{instance.product.sku}/{filename.lower()}'

class ProductsImages(models.Model):
    product = models.ForeignKey(Products, verbose_name='Товар', on_delete=models.CASCADE)
    image   = ProcessedImageField(verbose_name='Изображение',
                                upload_to=product_image_upload_path,
                                processors=[ResizeToFit(1920, 1080)],
                                format='JPEG',
                                options={'quality': 75},
                                blank=True, null=True)

    image_thumbnail = ImageSpecField(source='image',
                                    processors=[ResizeToFill(128, 100)],
                                    format='JPEG',
                                    options={'quality': 70})

    # Thumbnail for admin
    def image_thumb(self):
        return mark_safe(f'<img style="width: 386px; height: auto;" src="{self.image.url}" alt="">')
    image_thumb.short_description = 'Изображение (thumb)'
    # END Thumbnail for admin

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'



# @receiver(post_save, sender=Categories)
# def lowercase_category_slug(sender, instance, created, **kwargs):
@receiver(pre_save, sender=Categories)
def lowercase_category_slug(sender, instance, **kwargs):
    instance.slug = instance.slug.lower()