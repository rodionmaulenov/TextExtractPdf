from django import forms

from upload_file.models import Client


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('file_upload',)
