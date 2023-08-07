from django import forms

from upload_file.models import ClientExtractLocus


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = ClientExtractLocus
        fields = ('file_upload',)
