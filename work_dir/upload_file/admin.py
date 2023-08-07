from django.contrib import admin
from django.shortcuts import render, HttpResponseRedirect
from django.urls import path
from django.contrib import messages

from upload_file.forms import FileUploadForm
from upload_file.models import ClientExtractLocus


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'locus', 'file_upload')

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

        if request.method == 'POST':
            form = FileUploadForm(request.POST or None, request.FILES or None)
            pdf_file = request.FILES.get('file_upload')

            if not pdf_file.name.endswith('.pdf'):
                messages.warning(request, 'Wrong type file was uploaded')
                return HttpResponseRedirect(request.path_info)
            if form.is_valid():
                form.save()

        form = FileUploadForm()

        context = dict(
            self.admin_site.each_context(request),
            form=form
        )

        return render(request, template_name=template_name, context=context)


admin.site.register(ClientExtractLocus, ClientAdmin)
