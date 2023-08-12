from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect

from upload_file.forms import FileUploadForm, DnkForm
from upload_file.mixins import VerifyDnkMixin, ClientLogicPostMixin


class ClientView(View, VerifyDnkMixin, ClientLogicPostMixin):
    """Main view that uploaded files and submit text form"""
    template_name = 'admin/pdf_upload.html'  # Default template name
    form_class = FileUploadForm  # Upload form class
    dnk_form = DnkForm  # Locus form class

    def get(self, request):
        """Rendering a template with two forms"""
        form = self.form_class()
        dnk_form = self.dnk_form()
        context = self.get_context(form, dnk_form, request)
        return render(request, template_name=self.get_template_name(), context=context)

    def post(self, request):
        """Has Submitted one form or redirect to the same page"""
        if 'upload_form_submit' in request.POST:
            return self.handle_upload_form_submission(request, self.form_class, self.redirect_to)
        elif 'dnk_form_submit' in request.POST:
            return self.handle_dnk_form_submission(request, self.dnk_form, self.redirect_to, self.get_clients,
                                                   self.create_child, self.verify_data)

        return HttpResponseRedirect(request.path_info)

    def get_template_name(self):
        """either request.htmx either request"""
        if hasattr(self.request, 'htmx'):
            return 'admin/pdf_upload_htmx.html'
        return self.template_name

    def get_context(self, form, dnk_form, request):
        """Forms context from forms and admin.site"""
        context = dict(
            self.admin.admin_site.each_context(request),
            form=form,
            dnk_form=dnk_form
        )
        return context
