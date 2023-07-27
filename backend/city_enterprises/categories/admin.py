from django.contrib import admin

from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(Category, CategoryAdmin)
