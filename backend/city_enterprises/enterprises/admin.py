from django.contrib import admin

from .models import EnterpriseNetwork, Enterprise


class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'enterprise_network')
    search_fields = ('name', 'enterprise_network')


class EnterpriseNetworkAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    search_fields = ('name',)


admin.site.register(Enterprise, EnterpriseAdmin)
admin.site.register(EnterpriseNetwork, EnterpriseNetworkAdmin)
