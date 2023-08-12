from django.contrib import admin
from django.db.models import Count
from django.urls import path

from upload_file.models import Client, Child, DNK
from upload_file.views import ClientView


class ChildCountFilter(admin.SimpleListFilter):
    title = 'childs have'

    parameter_name = 'childs'

    def lookups(self, request, model_admin):
        dict_numbers = {
            0: 'zero',
            1: 'one',
            2: 'two',
            3: 'three',
            4: 'four',
        }
        lst = []
        for i in range(5):
            lst.append((str(i), f'{dict_numbers.get(i)} childs'))

        return lst

    def queryset(self, request, queryset):
        if self.value() == '0':
            queryset = queryset.annotate(childs=Count('child'))
            return queryset.filter(childs=0)
        if self.value() == '1':
            queryset = queryset.annotate(childs=Count('child'))
            return queryset.filter(childs=1)
        if self.value() == '2':
            queryset = queryset.annotate(childs=Count('child'))
            return queryset.filter(childs=2)
        if self.value() == '3':
            queryset = queryset.annotate(childs=Count('child'))
            return queryset.filter(childs=3)
        if self.value() == '4':
            queryset = queryset.annotate(childs=Count('child'))
            return queryset.filter(childs=4)


class ClientAdmin(admin.ModelAdmin):
    fields = ('name', 'locus', 'date_update', 'date_create', 'file_upload', 'childs')
    readonly_fields = ('name', 'date_update', 'date_create', 'file_upload', 'childs')
    list_display = ('name', 'date_update', 'date_create', 'file_upload', 'childs')
    search_fields = ('name__icontains',)
    list_filter = ('date_update', 'date_create', ChildCountFilter)

    def childs(self, obj):
        return obj.child_set.count()

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('form/', self.admin_site.admin_view(self.my_view))
        ]
        return my_urls + urls

    def my_view(self, request):
        view = ClientView
        view.admin = self  # send to class method ClientView instance of admin site for context
        view = view.as_view()
        return view(request)


admin.site.register(Client, ClientAdmin)
admin.site.register(Child)
admin.site.register(DNK)
