from django.contrib import admin

from .models import Categories, Products, ProductsImages


admin.site.register(Categories)

# admin.site.register(ProductsImages)

class ProductsImagesInline(admin.TabularInline):
    model = ProductsImages
    extra = 0
    max_num = 30
    readonly_fields = ('image_thumb',)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    inlines = [
        ProductsImagesInline,
    ]

    readonly_fields = ('main_image_thumb',)
    list_display = ('name', 'sku', 'active', 'updated')
    # list_editable = ('active',)
    list_filter = ('active',)
    search_fields = ('name', 'sku')
    ordering = ('-updated',)
    fields = ('active', 'sku', 'name', 'categories', 'price_discount', 'price', 'body', 'main_image_thumb', 'main_image')
