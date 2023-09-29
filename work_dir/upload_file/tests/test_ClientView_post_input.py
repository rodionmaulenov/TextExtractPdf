from django.contrib.auth.models import Group, User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from upload_file.models import Client


class MyAdminViewPostRequestDnkFormTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = '/admin/upload_file/client/form/'

    def setUp(self) -> None:
        self.tatu_vasile = Client.objects.create(name='Tasu Vasile',
                                                 locus={"FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                                                        "CSF1PO": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
                                                        "D2S441": "11,14", "D5S818": "13,13", "D7S82O": "12,12",
                                                        "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                                                        "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
                                                        "D3S1358": "15,16", "D6S1O43": "11,12", "D8S1179": "14,14",
                                                        "Penta D": "11,12", "Penta E": "12,13", "D1OS1248": "15,15",
                                                        "D22S1O45": "15,15"})

        self.tiganis_nicholas = Client.objects.create(name='Tiganis Nicholas',
                                                      locus={"FGA": "19,24", "vWA": "16,18", "THO1": "6,9.3",
                                                             "TPOX": "8,9",
                                                             "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
                                                             "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
                                                             "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "17,24",
                                                             "D3S1358": "15,17", "D8S1179": "10,15"})

        self.user = User.objects.create_user(username='testuser', password='password', is_staff=True)

        group1 = Group.objects.create(name='users_input_text')
        group2 = Group.objects.create(name='users_upload')
        self.user.groups.add(group1, group2)

        self.client.login(username='testuser', password='password')

    def test_post_valid_dnk_form_mother_and_child(self):
        data = {
            'dnk_form_submit': '',
            "FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
            "CSF1PO": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
            "D2S441": "11,14", "D5S818": "13,13", "D7S82O": "12,12",
            "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
            "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
            "D3S1358": "15,16", "D6S1O43": "11,12", "D8S1179": "14,14",
            "Penta D": "11,12", "Penta E": "12,13", "D1OS1248": "15,15",
            "D22S1O45": "15,15"
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)

        change_url_admin = reverse(
            'admin:%s_%s_change' % (self.tatu_vasile._meta.app_label, self.tatu_vasile._meta.model_name),
            args=[self.tatu_vasile.pk])

        self.assertEqual(str(messages[0]),
                         f'Father instance <a href="{change_url_admin}">{self.tatu_vasile.name.upper()}</a> match')

    def test_post_valid_dnk_form_no_match_mother_and_child(self):
        data = {
            'dnk_form_submit': '',
            "FGA": "40,40", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
            "CSF1PO": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
            "D2S441": "11,14", "D5S818": "13,13", "D7S82O": "12,12",
            "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
            "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
            "D3S1358": "15,16", "D6S1O43": "11,12", "D8S1179": "14,14",
            "Penta D": "11,12", "Penta E": "12,13", "D1OS1248": "15,15",
            "D22S1O45": "15,15"
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)

        change_url_admin = reverse(
            'admin:%s_%s_change' % (self.tatu_vasile._meta.app_label, self.tatu_vasile._meta.model_name),
            args=[self.tatu_vasile.pk])

        self.assertEqual(str(messages[0]),'Matching not found.')

    def test_valid_dnk_form_with_valid_dnk_data_eurolab(self):
        data = {
            'dnk_form_submit': '',
            "FGA": "19,24", "vWA": "16,18", "THO1": "6,9.3",
            "TPOX": "8,9",
            "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
            "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
            "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "17,24",
            "D3S1358": "15,17", "D8S1179": "10,15",
            # this is unnecessary locus
            'Penta E': "15,17", 'D2S441': "15,17", 'D22S1O45': "15,17",
            'D6S1O43': "15,17", 'D1OS1248': "15,17", 'D1S1656': "15,17",
            'D12S391': "15,17", 'Penta D': "15,17"
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)

        change_url_admin = reverse(
            'admin:%s_%s_change' % (self.tiganis_nicholas._meta.app_label, self.tiganis_nicholas._meta.model_name),
            args=[self.tiganis_nicholas.pk])

        self.assertEqual(str(messages[0]),
                         f'Father instance <a href="{change_url_admin}">{self.tiganis_nicholas.name.upper()}</a> match')

    def test_valid_dnk_form_no_match_eurolab(self):
        data = {
            'dnk_form_submit': '',
            "FGA": "15,5", "vWA": "16,18", "THO1": "6,9.3",
            "TPOX": "8,9",
            "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
            "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
            "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "17,24",
            "D3S1358": "15,17", "D8S1179": "10,15",
            # this is unnecessary locus
            'Penta E': "15,17", 'D2S441': "15,17", 'D22S1O45': "15,17",
            'D6S1O43': "15,17", 'D1OS1248': "15,17", 'D1S1656': "15,17",
            'D12S391': "15,17", 'Penta D': "15,17"
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)

        change_url_admin = reverse(
            'admin:%s_%s_change' % (self.tiganis_nicholas._meta.app_label, self.tiganis_nicholas._meta.model_name),
            args=[self.tiganis_nicholas.pk])

        self.assertEqual(str(messages[0]),'Matching not found.')

    def test_valid_dnk_form_empty_field(self):
        data = {
            'dnk_form_submit': '',
            "FGA": "19,24", "vWA": "16,18", "THO1": "6,9.3",
            "TPOX": "8,9",
            "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
            "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
            "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "17,24",
            "D3S1358": "15,17", "D8S1179": "10,15",
            # this is unnecessary locus
            'Penta E': "15,17", 'D2S441': "15,17", 'D22S1O45': "15,17",
            'D6S1O43': "15,17", 'D1OS1248': "15,17", 'D1S1656': "15,17",
            # this is empty field
            'D12S391': "15,17", 'Penta D': ""
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)

        self.assertEqual(str(messages[0]),'Form lines can not be a empty')

    def test_valid_dnk_form_not_contain_numbers_and_dot_field(self):
        data = {
            'dnk_form_submit': '',
            # not contain only numbers and dot
            "FGA": "19fff,24", "vWA": "16,18", "THO1": "6,9.3",
            "TPOX": "8,9",
            "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
            "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
            "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "17,24",
            "D3S1358": "15,17", "D8S1179": "10,15",
            # this is unnecessary locus
            'Penta E': "15,17", 'D2S441': "15,17", 'D22S1O45': "15,17",
            'D6S1O43': "15,17", 'D1OS1248': "15,17", 'D1S1656': "15,17",
            'D12S391': "15,17", 'Penta D': "15,17"
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)

        self.assertEqual(str(messages[0]), 'Number should contain only 0123456789.')

    def test_valid_dnk_form_not_two_numbers_separated_by_comma_in_field(self):
        data = {
            'dnk_form_submit': '',
            # not contain two numbers separated by a comma
            "FGA": "19.24.34", "vWA": "16,18", "THO1": "6,9.3",
            "TPOX": "8,9",
            "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
            "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
            "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "17,24",
            "D3S1358": "15,17", "D8S1179": "10,15",
            # this is unnecessary locus
            'Penta E': "15,17", 'D2S441': "15,17", 'D22S1O45': "15,17",
            'D6S1O43': "15,17", 'D1OS1248': "15,17", 'D1S1656': "15,17",
            'D12S391': "15,17", 'Penta D': "15,17"
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)

        self.assertEqual(str(messages[0]), 'Only two numbers separated by a comma')
