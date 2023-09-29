from django import forms

from upload_file.models import Client

locus_from_mother_and_child = ['D3S1358', 'vWA', 'D16S539', 'CSF1PO', 'TPOX', 'D8S1179', 'D21S11', 'D18S51', 'Penta E',
                               'D2S441', 'D19S433', 'THO1', 'FGA', 'D22S1O45', 'D5S818', 'D13S317', 'D7S82O', 'D6S1O43',
                               'D1OS1248', 'D1S1656', 'D12S391', 'D2S1338', 'Penta D']


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('file_upload',)


class LocusForm(forms.Form):
    for locus_name in locus_from_mother_and_child:
        locals()[locus_name] = forms.CharField(max_length=100, required=False)
