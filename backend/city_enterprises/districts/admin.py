from django.contrib import admin

from .models import CityDistrict


class CityDistrictAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)


admin.site.register(CityDistrict, CityDistrictAdmin)
