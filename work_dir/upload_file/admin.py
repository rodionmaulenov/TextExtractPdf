from django.contrib import admin
from upload_file.models import Client


class ClientAdmin(admin.ModelAdmin):
    fields = ('name', 'locus', 'date_update', 'date_create', 'file')
    readonly_fields = ('name', 'date_update', 'date_create', 'file')
    list_display = ('name', 'count_locus', 'date_update', 'date_create', 'file')
    search_fields = ('name__icontains',)
    list_filter = ('date_update', 'date_create')
    list_per_page = 20

    def count_locus(self, obj):
        if obj.locus:
            return len(obj.locus)
        return 0

    count_locus.short_description = 'Number of Locus'


admin.site.register(Client, ClientAdmin)
