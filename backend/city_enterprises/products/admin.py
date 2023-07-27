from django.contrib import admin

from .models import Product, ProductPrice


class ProductPriceInline(admin.TabularInline):
    model = ProductPrice
    extra = 1
    fields = ('enterprise', 'price')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'enterprise_network')
    search_fields = ('name',)
    inlines = [ProductPriceInline]


admin.site.register(Product, ProductAdmin)
