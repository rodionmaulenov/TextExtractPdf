from django.contrib import admin
from upload_file.models import Client


class ClientAdmin(admin.ModelAdmin):
    fields = ('name', 'locus', 'date_update', 'date_create', 'file_upload')
    readonly_fields = ('name', 'date_update', 'date_create', 'file_upload')
    list_display = ('name', 'date_update', 'date_create', 'file_upload')
    search_fields = ('name__icontains',)
    list_filter = ('date_update', 'date_create')


admin.site.register(Client, ClientAdmin)
