from django.urls import reverse

from upload_file.models import Client

from django.contrib import messages
from django.utils.safestring import mark_safe

locus = ['D3S1358', 'vWA', 'D16S539', 'CSF1PO', 'TPOX', 'D8S1179', 'D21S11', 'D18S51', 'Penta E',
         'D2S441', 'D19S433', 'THO1', 'FGA', 'D22S1O45', 'D5S818', 'D13S317', 'D7S82O', 'D6S1O43',
         'D1OS1248', 'D1S1656', 'D12S391', 'D2S1338', 'Penta D']


class CompareLocusMixin:
    def get_link(self, father):
        change_url_admin = reverse(
            'admin:%s_%s_change' % (father._meta.app_label, father._meta.model_name),
            args=[father.pk])
        return change_url_admin

    def compare_dnk(self, request, form):
        """Find father by locus child"""
        for father_instance in Client.objects.all():
            father_dnk = father_instance.locus

            child_dnk = [(name, form.cleaned_data.get(name)) for name in locus]
            if len(father_dnk) == 15:
                exclude = ['Penta E', 'D2S441', 'D22S1O45', 'D6S1O43', 'D1OS1248', 'D1S1656', 'D12S391', 'Penta D']
                child_dnk = [(name, value) for name, value in child_dnk if name not in exclude]

            list_matching = []
            for key, value in child_dnk:
                if key in father_dnk:
                    child_value = value.split(',')
                    father_value = father_dnk[key]

                    father_locus = [num.strip() for num in father_value.split(',')]
                    list_matching.append(any(num.strip() in father_locus for num in child_value))

            if all(list_matching) and len(list_matching) > 1:
                change_url_admin = self.get_link(father_instance)
                messages.success(request, mark_safe(
                    f'father <a href="{change_url_admin}">{father_instance.name.title()}</a>'))
            else:
                messages.info(request, 'not matching')
                list_matching = []

