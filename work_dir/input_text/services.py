from django.urls import reverse

from upload_file.models import Client

from django.contrib import messages
from django.utils.safestring import mark_safe

locus = {'D3S1358', 'vWA', 'D16S539', 'CSF1PO', 'TPOX', 'D8S1179', 'D21S11', 'D18S51', 'Penta E',
         'D2S441', 'D19S433', 'THO1', 'FGA', 'D22S1O45', 'D5S818', 'D13S317', 'D7S82O', 'D6S1O43',
         'D1OS1248', 'D1S1656', 'D12S391', 'D2S1338'}


class CompareLocusMixin:
    def get_link(self, father):
        change_url_admin = reverse(
            'admin:%s_%s_change' % (father._meta.app_label, father._meta.model_name),
            args=[father.pk])
        return change_url_admin

    def compare_dnk(self, form):
        """Find father by locus child"""

        match = []
        total = {}
        for father_instance in Client.objects.all():
            father_dnk = father_instance.locus

            child_dnk = [
                (name, form.cleaned_data.get(name, '')
                if form.cleaned_data.get(name, '') else '')
                for name in locus
            ]

            for key, value_f in father_dnk.items():
                for key_ch, value_ch in child_dnk:
                    if key_ch == key and value_ch and value_f:

                        value_ch = value_ch.replace(' ', '').split(',')

                        for num in value_ch:
                            if num in value_f.split(','):
                                match.append(1)
                                break

            if len(father_dnk) < len(child_dnk) and len(match) == len(father_dnk):
                total[father_instance] = len(match)
            elif len(father_dnk) < len(child_dnk) and (len(father_dnk) - len(match)) == 1:
                total[father_instance] = len(match)
            elif len(father_dnk) >= len(child_dnk) and len(match) == len(child_dnk):
                total[father_instance] = len(match)
            elif len(father_dnk) >= len(child_dnk) and (len(child_dnk) - len(match)) == 1:
                total[father_instance] = len(match)

            match = []

        return total

    def get_message(self, request, total):
        if total:
            for father, match in total.items():
                change_url_admin = self.get_link(father)
                messages.success(request, mark_safe(
                    f'<span class="success-message"><a href="{change_url_admin}">'
                    f'{father.name.title()} {match}</a></span>'))
        else:
            messages.info(request, '<span class="info-message">not matching</span>')


# from django.db.models import Q
#
# class CompareLocusMixinV1:
#     def get_link(self, father):
#         change_url_admin = reverse('admin:%s_%s_chanin message.messagege' % (father._meta.app_label, father._meta.model_name), args=[father.pk])
#         return change_url_admin
#
#     def compare_dnk(self, form):
#         """Find fathers by locus child"""
#
#         # Create a dictionary to store child's DNK
#         child_dnk = {name: form.cleaned_data.get(name, '') for name in locus}
#
#         # Create a Q object for filtering fathers
#         filter_q = Q()
#         for key, value in child_dnk.items():
#             filter_q |= Q(locus__contains={key: value})
#
#         # Filter fathers based on the child's DNK
#         matching_fathers = Client.objects.filter(filter_q)
#
#         # Create a dictionary to store matching fathers and their match counts
#         total = {}
#         for father_instance in matching_fathers:
#             father_dnk = father_instance.locus
#             match_count = sum(1 for key, value in child_dnk.items() if father_dnk.get(key, '') == value)
#             total[father_instance] = match_count
#
#         return total
#
#     def get_message(self, request, total):
#         if total:
#             for father, match in total.items():
#                 change_url_admin = self.get_link(father)
#                 messages.success(request,
#                                  mark_safe(f'<span class="success-message"><a href="{change_url_admin}">'
#                                            f'{father.name.title()} {match}</a></span>')
#                                  )
#         else:
#             messages.info(request, '<span class="info-message">not matching</span>')
