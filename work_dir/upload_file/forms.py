from django import forms

from upload_file.models import Client, DNK


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('file_upload',)


class DnkForm(forms.ModelForm):
    class Meta:
        model = DNK
        fields = ['D3S1358', 'vWA', 'D16S539', 'CSF1P0', 'TPOX', 'D8S1179', 'D21S11', 'D18S51', 'Penta_E', 'D2S441',
                  'D19S433', 'THO1', 'FGA', 'D22S1045', 'D5S818', 'D13S317', 'D7S820', 'D6S1043', 'D10S1248', 'D1S1656',
                  'D12S391', 'D2S1338', 'Penta_D']
