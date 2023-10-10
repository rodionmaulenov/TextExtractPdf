from django.contrib.auth.models import Group, User
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages

from upload_file.models import Client as Father


class PostInputTextViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword', is_staff=True)
        group1 = Group.objects.create(name='users_input_text')
        group2 = Group.objects.create(name='users_upload')
        group1.user_set.add(self.user)
        group2.user_set.add(self.user)
        self.client.login(username='testuser', password='testpassword')

    def test_post_found_matching_all_locus_match(self):
        url = reverse('input_text')

        Father.objects.create(name='Tasu Vasile',
                              locus={"FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                                     "CSF1PO": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
                                     "D2S441": "11,14", "D5S818": "13,13", "D7S82O": "12,12",
                                     "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                                     "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
                                     "D3S1358": "15,16", "D6S1O43": "11,12", "D8S1179": "14,14",
                                     "Penta E": "12,13", "D1OS1248": "15,15",
                                     "D22S1O45": "15,15"})

        data = {"FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                "CSF1PO": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
                "D2S441": "11,14", "D5S818": "13,13", "D7S82O": "12,12",
                "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
                "D3S1358": "15,16", "D6S1O43": "11,12", "D8S1179": "14,14",
                "Penta E": "12,13", "D1OS1248": "15,15",
                "D22S1O45": "15,15"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any('father <a href="/admin/upload_file/client/2/change/">Tasu Vasile</a>'
                in message.message for message in messages)
        )

    def test_another_post_found_matching_one_locus_not_match(self):
        url = reverse('input_text')

        Father.objects.create(name='Pislaru Madalin',
                              locus={"D3S1358": "14,16", "vWA": "14,16", "D16S539": "11,12", "CSF1PO": "10,11",
                                     "TPOX": "8,9", "D8S1179": "12,15", "D21S11": "29,29", "D18S51": "17,20",
                                     "Penta E": "7,17", "D2S441": "10,10", "D19S433": "12,15", "THO1": "7,9",
                                     "FGA": "19,23", "D22S1O45": "15,15", "D5S818": "12,13", "D13S317": "9,12",
                                     "D7S82O": "11,11", "D6S1O43": "17,18", "D1OS1248": "13,16", "D1S1656": "11,12",
                                     "D12S391": "18,18", "D2S1338": "18,24"})
        # not match "vWA": "1,1"
        data = {"D3S1358": "14,1", "vWA": "1,1", "D16S539": "0,12", "CSF1PO": "4,11", "TPOX": "4.4,9",
                "D8S1179": "5,15", "D21S11": "29,19", "D18S51": "17,20", "Penta E": "7.4,17", "D2S441": "1,10",
                "D19S433": "12,1", "THO1": "7.34,9", "FGA": "19.25,23", "D22S1O45": "15.1,15", "D5S818": "3,13",
                "D13S317": "8,12", "D7S82O": "1,11", "D6S1O43": "7,18", "D1OS1248": "3,16", "D1S1656": "11,2",
                "D12S391": "8,18", "D2S1338": "18,24.1"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any('father <a href="/admin/upload_file/client/1/change/">Pislaru Madalin</a>'
                in message.message for message in messages)
        )

    def test_post_found_matching_eurolab(self):
        url = reverse('input_text')

        Father.objects.create(name='Tiganis Nicholas',
                              locus={"FGA": "19,24", "vWA": "16,18", "THO1": "6,9.3",
                                     "TPOX": "8,9", "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
                                     "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
                                     "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "17,24",
                                     "D3S1358": "15,17", "D8S1179": "10,15"})

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
            'D12S391': "15,17"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any('father <a href="/admin/upload_file/client/3/change/">Tiganis Nicholas</a>'
                in message.message for message in messages)
        )

    def test_post_not_found_matching(self):
        url = reverse('input_text')

        Father.objects.create(name='Tasu Vasile',
                              locus={"FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                                     "CSF1PO": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
                                     "D2S441": "11,14", "D5S818": "13,13", "D7S82O": "12,12",
                                     "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                                     "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
                                     "D3S1358": "15,16", "D6S1O43": "11,12", "D8S1179": "14,14",
                                     "Penta E": "12,13", "D1OS1248": "15,15", "D22S1O45": "15,15"})
        # change FGA, vWA
        data = {"FGA": "1,1", "vWA": "10,10", "THO1": "8,9", "TPOX": "8,8",
                "CSF1PO": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
                "D2S441": "11,14", "D5S818": "13,13", "D7S82O": "12,12",
                "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
                "D3S1358": "15,16", "D6S1O43": "11,12", "D8S1179": "14,14",
                "Penta E": "12,13", "D1OS1248": "15,15", "D22S1O45": "15,15"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('not matching' in message.message for message in messages))
