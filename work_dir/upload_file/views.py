from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from home_api.decorators import optimized_view_decorator
from upload_file.services import ProcessUploadedFileMixin


@method_decorator(
    decorator=optimized_view_decorator(['users_input_text', 'users_upload']),
    name='dispatch'
)
class FileUploadView(ProcessUploadedFileMixin, View):
    """Processing the logic uploaded files"""

    def get(self, request, *args, **kwargs):
        return render(request, 'upload_file/upload_form.html')

    def post(self, request, *args, **kwargs):
        responses = []

        for _, uploaded_file in request.FILES.items():
            response = self.process_uploaded_file(uploaded_file)
            responses.append(response)

        return JsonResponse(responses, status=200, safe=False)
