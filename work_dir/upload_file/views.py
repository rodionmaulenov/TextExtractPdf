from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from home_api.decorators import optimized_view_decorator
from upload_file.services import (AwsMotherAndChild, ProcessUploadedFile, PdfPlumberMotherAndChild,
                                  AwsEvrolab, AwsMotherAndChildV2)


@method_decorator(
    decorator=optimized_view_decorator(['users_input_text', 'users_upload']),
    name='dispatch'
)
class FileUploadView(View):
    """Processing the logic uploaded files"""

    handler = ProcessUploadedFile

    def get(self, request, *args, **kwargs):
        return render(request, 'upload_file/upload_form.html')

    def post(self, request, *args, **kwargs):
        responses = []

        instance_list = [
            PdfPlumberMotherAndChild, AwsEvrolab, AwsMotherAndChild, AwsMotherAndChildV2
        ]

        for _, uploaded_file in request.FILES.items():
            process_file = self.handler(uploaded_file, instance_list)
            obtaining_dict = process_file.process_uploaded_file()
            message = process_file.message_response(obtaining_dict)
            process_file.clean_up_files()
            responses.append(message)

        return JsonResponse(responses, status=200, safe=False)
