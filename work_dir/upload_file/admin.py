from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.safestring import mark_safe

from upload_file.decorators import user_in_group
from upload_file.forms import FileUploadForm, LocusForm
from upload_file.models import Client
from upload_file.services import verify_form_fields, get_table_from_pdf_file, compare_dnk_child_with_father


class ClientAdmin(admin.ModelAdmin):
    fields = ('name', 'date_update', 'date_create', 'file_upload')
    readonly_fields = ('name', 'date_update', 'date_create', 'file_upload')
    list_display = ('name', 'date_update', 'date_create', 'file_upload')
    search_fields = ('name__icontains',)
    list_filter = ('date_update', 'date_create')

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

        def redirect_home(request):
            return redirect(request.path_info)

        if request.method == 'POST':

            if 'upload_form_submit' in request.POST:
                uploaded_files = request.FILES.getlist('file_upload')
                for pdf_file in uploaded_files:
                    if pdf_file.name.endswith('.pdf'):
                        try:
                            locus_dict, name = get_table_from_pdf_file(request, pdf_file)
                        except Exception:
                            messages.error(request, f'Error processing file: {pdf_file.name}')
                            continue

                        if locus_dict and name:
                            father, created = Client.objects.get_or_create(name=name, locus=locus_dict)

                            if not created:
                                messages.warning(request,
                                                 f'Exactly the same client {name} already exists for file: {pdf_file.name}')
                            else:
                                father.name = name
                                father.locus = locus_dict
                                father.file_upload = pdf_file
                                father.save()

                                messages.success(request,
                                                 f'Client instance {name} saved successfully from file: {pdf_file.name}')
                        else:
                            messages.warning(request, f"Returned None for file: {pdf_file.name}. Blank name or dict")

                    else:
                        messages.warning(request, f'Invalid file extension for file: {pdf_file.name}')

                return redirect_home(request)

            if 'dnk_form_submit' in request.POST:
                dnk_form = LocusForm(request.POST)
                if dnk_form.is_valid():
                    child_dnk = dnk_form.cleaned_data.items()
                    verify = verify_form_fields(request, child_dnk)

                    if verify:
                        father = compare_dnk_child_with_father(child_dnk)

                        if father:
                            change_url_admin = reverse(
                                'admin:%s_%s_change' % (father._meta.app_label, father._meta.model_name),
                                args=[father.pk])
                            messages.success(request, mark_safe(
                                f'Father instance <a href="{change_url_admin}">{father.name.upper()}</a> match'))
                            return redirect_home(request)
                        else:
                            messages.error(request, 'Matching not found.')
                            return redirect_home(request)
                    else:
                        return redirect_home(request)

        form = FileUploadForm()
        dnk_form = LocusForm()
        context = dict(
            self.admin_site.each_context(request),
            form=form,
            dnk_form=dnk_form,
        )

        return TemplateResponse(request, template_name, context)


admin.site.register(Client, ClientAdmin)
