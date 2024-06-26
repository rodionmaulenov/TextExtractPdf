from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from home_api.decorators import optimized_view_decorator
from upload_file.services import (AwsMotherAndChild, ProcessUploadedFile, AwsEvrolabV2,
                                  AwsMotherAndChildV2, AwsMotherAndChildV3, AwsEvrolab)


@method_decorator(
    decorator=optimized_view_decorator(['users_input_text', 'users_upload']),
    name='dispatch'
)
class FileUploadView(View):
    """Processing the logic uploaded files"""

    handler = ProcessUploadedFile

    def get(self, request):
        return render(request, 'upload_file/upload_form.html')

    def post(self, request):
        responses = []

        instance_list = [
            AwsMotherAndChild, AwsMotherAndChildV2, AwsMotherAndChildV3,
            AwsEvrolab, AwsEvrolabV2,
        ]

        for _, uploaded_file in request.FILES.items():
            instance = self.handler(uploaded_file, instance_list, 'image_jpg')
            obtaining_dict = instance.process_file()
            message = instance.message_response(obtaining_dict)
            instance.clean_folder()
            responses.append(message)

        return JsonResponse(responses, status=200, safe=False)
