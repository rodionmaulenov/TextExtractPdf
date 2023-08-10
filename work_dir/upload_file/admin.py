from django.contrib import admin
from django.db.models import Count
from django.shortcuts import render, HttpResponseRedirect
from django.urls import path
from django.contrib import messages
from django.forms.models import inlineformset_factory

from upload_file.forms import FileUploadForm
from upload_file.models import Client, Child, DNK
from upload_file.services import pdf_extract_text, retrieve_values, get_dict_from_instances, find_father_by_locus, \
    verify_data


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
    fields = ('name', 'date_update', 'date_create', 'file_upload', 'childs')
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

        template_name = 'admin/pdf_upload.html'
        if hasattr(request, 'htmx'):
            template_name = 'admin/pdf_upload_htmx.html'

        LocusFormSet = inlineformset_factory(Child, DNK, extra=1, can_delete=False, fields=('locus', 'data'))
        child = None
        if 'formset_submit' in request.POST:
            child = Child.objects.create()

        if request.method == 'POST':
            form = FileUploadForm(request.POST or None, request.FILES or None)
            formset = LocusFormSet(request.POST or None, instance=child)

            if 'form_submit' in request.POST:
                pdf_file = request.FILES.get('file_upload')

                if not pdf_file.name.endswith('.pdf'):
                    messages.warning(request, 'Wrong type file was uploaded. Must been in format PDF')
                    return HttpResponseRedirect(request.path_info)

                if form.is_valid():
                    path_to_record = pdf_extract_text(pdf_file)
                    name, locus_dict = retrieve_values(path_to_record)
                    obj, _ = Client.objects.get_or_create(name=name, locus=locus_dict)
                    if not _:
                        messages.warning(request, f'Exactly the same client {name} already exists')
                        return HttpResponseRedirect(request.path_info)

                    if _:
                        obj.file_upload = pdf_file
                        obj.save()
                        messages.success(request, f'Client instance {name} save successfully')
                        return HttpResponseRedirect(request.path_info)
                else:
                    messages.error(request, 'Form is not valid. Please check the uploaded file.')
                    return HttpResponseRedirect(request.path_info)

            elif 'formset_submit' in request.POST:
                if formset.is_valid():
                    objs_dnk = formset.save()
                    validator = verify_data(request, objs_dnk, child)
                    if validator:
                        clients = Client.objects.all()
                        child_locus_dict = get_dict_from_instances(objs_dnk)
                        client_obj = find_father_by_locus(child_locus_dict, clients)

                        if client_obj:
                            snippet_name = str(1) if client_obj.child_set.count() == 0 else str(
                                client_obj.child_set.count() + 1)
                            child.name = client_obj.name + ' child ' + snippet_name
                            child.client = client_obj
                            child.save()
                            child.dnk_set.all().delete()
                            messages.success(request, f'We have matching father {client_obj.name.upper()}')
                            return HttpResponseRedirect(request.path_info)

                        else:
                            child.dnk_set.all().delete()
                            child.delete()
                            messages.error(request, f'Matching not found')
                            return HttpResponseRedirect(request.path_info)
                    else:
                        return HttpResponseRedirect(request.path_info)

                else:
                    messages.error(request, 'Form populated is not valid. Please check the form entries.')
                    child.delete()
                    return HttpResponseRedirect(request.path_info)

        form = FileUploadForm()
        formset = LocusFormSet()

        context = dict(
            self.admin_site.each_context(request),
            form=form,
            formset=formset
        )

        return render(request, template_name=template_name, context=context)


admin.site.register(Client, ClientAdmin)
admin.site.register(Child)
admin.site.register(DNK)
