from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from django.core.files.base import ContentFile

from upload_file.decorators import user_in_group
from upload_file.forms import FileUploadForm, DnkForm
from upload_file.models import Client, Child, DNK
from upload_file.services import pdf_extract_text, retrieve_values, get_dict_from_instances, \
    compare_dnk_child_with_clients, verify_data


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
        if self.value() is not None:
            value = int(self.value())

            if value >= 0 and value <= 4:
                queryset = queryset.annotate(childs=Count('child'))
                return queryset.filter(childs=value)

        return queryset
    # def queryset(self, request, queryset):
    #     if self.value() == '0':
    #         queryset = queryset.annotate(childs=Count('child'))
    #         return queryset.filter(childs=0)
    #     if self.value() == '1':
    #         queryset = queryset.annotate(childs=Count('child'))
    #         return queryset.filter(childs=1)
    #     if self.value() == '2':
    #         queryset = queryset.annotate(childs=Count('child'))
    #         return queryset.filter(childs=2)
    #     if self.value() == '3':
    #         queryset = queryset.annotate(childs=Count('child'))
    #         return queryset.filter(childs=3)
    #     if self.value() == '4':
    #         queryset = queryset.annotate(childs=Count('child'))
    #         return queryset.filter(childs=4)


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

    @user_in_group('users_input_text', 'users_upload')
    def my_view(self, request):
        template_name = 'admin/custom_base.html'

        def redirect_to(request):
            return redirect(request.path_info)

        if request.method == 'POST':
            if 'upload_form_submit' in request.POST:
                form = FileUploadForm(request.POST, request.FILES)
                if form.is_valid():
                    pdf_file = form.cleaned_data['file_upload']
                    if not pdf_file.name.endswith('.pdf'):
                        messages.warning(request, 'Wrong type file was uploaded. Must be in PDF format')
                        return redirect_to(request)

                    path_to_record = pdf_extract_text(pdf_file)  # extract locus data from upload pdf to csv_file
                    if path_to_record is None:
                        messages.warning(request, 'Must be a pdf file with locus table')
                        return redirect_to(request)
                    name, locus_dict = retrieve_values(
                        path_to_record)  # get client name and dnk locus client in format dict
                    obj, created = Client.objects.get_or_create(name=name, locus=locus_dict)

                    if not created:
                        messages.warning(request, f'Exactly the same client {name} already exists')
                        return redirect_to(request)

                    # obj.file_upload = pdf_file  # add pdf file to instance Client
                    # obj.save()
                    obj.file_upload.save(pdf_file.name, ContentFile(pdf_file.read()))
                    messages.success(request, f'Client instance {name} saved successfully')
                    return redirect_to(request)
                else:
                    messages.error(request, 'Form is not valid. Please check the uploaded file.')
                    return redirect_to(request)

            if 'dnk_form_submit' in request.POST:
                dnk_form = DnkForm(request.POST)
                child = Child.objects.create()

                if dnk_form.is_valid():
                    obj_dnk = dnk_form.save(commit=False)
                    obj_dnk.child = child
                    obj_dnk.save()  # assign relation 1_to_1 model child to dnk
                    verify = verify_data(request, obj_dnk, child)  # verify input form data

                    if verify:
                        clients = Client.objects.all()
                        child_locus_dict = get_dict_from_instances(
                            obj_dnk)  # retrieve data from instance and convert into dict
                        client_obj = compare_dnk_child_with_clients(child_locus_dict,
                                                                    clients)  # identify matching client and child dnk locus

                        if client_obj:
                            snippet_name = str(1) if client_obj.child_set.count() == 0 else str(
                                client_obj.child_set.count() + 1)
                            child.name = client_obj.name + ' child ' + snippet_name  # create name child instance
                            child.client = client_obj  # add relationship 1_to_many
                            child.save()
                            child.dnk.delete()  # has removed unnecessary instance dnk
                            messages.success(request, f'We have matching father {client_obj.name.upper()}')
                            return redirect_to(request)
                        else:
                            child.dnk.delete()  # if not have matching in verifying client and child instances removed dnk related vith child
                            child.delete()  # if not have matching in verifying client and child instances removed child obj
                            messages.error(request, 'Matching not found. Maybe you enter invalid data')
                            return redirect_to(request)
                else:
                    messages.error(request, 'DNK form is not valid. Please check the form entries.')

            return redirect_to(request)

        form = FileUploadForm()
        dnk_form = DnkForm()
        context = dict(
            self.admin_site.each_context(request),
            form=form,
            dnk_form=dnk_form
        )

        return TemplateResponse(request, template_name, context)


admin.site.register(Client, ClientAdmin)
admin.site.register(Child)
admin.site.register(DNK)
