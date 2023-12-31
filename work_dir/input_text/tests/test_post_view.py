from django.contrib.auth.models import Group, User
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages

from input_text.forms import LocusForm
from input_text.services import CompareLocusMixin
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

    def tearDown(self):
        Father.objects.all().delete()

    def test_post_found_matching_all_locus_match(self):
        """
        22 father locus
        22 child locus
        """
        url = reverse('input_text')

        Father.objects.create(id=8, name='Tasu Vasile',
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
            any('<a href="/admin/upload_file/client/8/change/">Tasu Vasile 22</a>'
                in message.message for message in messages)
        )

    def test_another_post_found_matching_one_locus_not_match(self):
        """
        22 father locus
        22 child locus
        """

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
            any('<a href="/admin/upload_file/client/1/change/">Pislaru Madalin 21</a>'
                in message.message for message in messages)
        )

    def test_post_found_matching_eurolab(self):
        """
        15 father locus
        22 child locus
        """
        url = reverse('input_text')

        Father.objects.create(id=9, name='Tiganis Nicholas',
                              locus={"FGA": "19,24", "vWA": "16,18", "THO1": "6,9.3",
                                     "TPOX": "8,9", "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
                                     "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
                                     "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "17,24",
                                     "D3S1358": "15,17", "D8S1179": "10,15"})

        data = {
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
            any('<a href="/admin/upload_file/client/9/change/">Tiganis Nicholas 15</a>'
                in message.message for message in messages)
        )

    def test_post_found_matching_eurolab_1_locus_fail(self):
        """
        15 father locus
        22 child locus
        """

        url = reverse('input_text')

        Father.objects.create(id=10, name='Tiganis Nicholas',
                              locus={"FGA": "19,24", "vWA": "16,18", "THO1": "6,9.3",
                                     "TPOX": "8,9", "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
                                     "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
                                     "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "17,24",
                                     "D3S1358": "15,17", "D8S1179": "10,15"})

        data = {
            # FGA
            "FGA": "0,0", "vWA": "16,18", "THO1": "6,9.3",
            "TPOX": "8,9", "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
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
            any('<a href="/admin/upload_file/client/10/change/">Tiganis Nicholas 14</a>'
                in message.message for message in messages)
        )

    def test_post_found_matching_eurolab_2_locus_fail(self):
        """
        15 father locus
        22 child locus
        """

        url = reverse('input_text')

        Father.objects.create(name='Tiganis Nicholas',
                              locus={"FGA": "19,24", "vWA": "16,18", "THO1": "6,9.3",
                                     "TPOX": "8,9", "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
                                     "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
                                     "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "17,24",
                                     "D3S1358": "15,17", "D8S1179": "10,15"})

        data = {
            # FGA
            "FGA": "0,0", "vWA": "0,0", "THO1": "6,9.3",
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
        self.assertTrue(any('not matching' in message.message for message in messages))

    def test_post_not_found_matching_22_locus_2_locus_fail(self):
        """
        15 father locus
        22 child locus
        """

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
        data = {"FGA": "0,0", "vWA": "10,10", "THO1": "8,9", "TPOX": "8,8",
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

    def test_post_found_few_matching_22_locus_1_locus_fail_mother_and_child(self):
        """
        22 father locus
        22 child locus
        """

        Father.objects.create(name='Tasu Vasile',
                              # change FGA
                              locus={"FGA": "21,22", "vWA": "10,10", "THO1": "8,9", "TPOX": "8,8",
                                     "CSF1PO": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
                                     "D2S441": "11,14", "D5S818": "13,13", "D7S82O": "12,12",
                                     "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                                     "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
                                     "D3S1358": "15,16", "D6S1O43": "11,12", "D8S1179": "14,14",
                                     "Penta E": "12,13", "D1OS1248": "15,15", "D22S1O45": "15,15"})

        Father.objects.create(name='Papa Karlo',
                              # vWa
                              locus={"FGA": "10,10", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                                     "CSF1PO": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
                                     "D2S441": "11,14", "D5S818": "13,13", "D7S82O": "12,12",
                                     "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                                     "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
                                     "D3S1358": "15,16", "D6S1O43": "11,12", "D8S1179": "14,14",
                                     "Penta E": "12,13", "D1OS1248": "15,15", "D22S1O45": "15,15"})

        data = {"FGA": "10,10", "vWA": "10,10", "THO1": "8,9", "TPOX": "8,8",
                "CSF1PO": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
                "D2S441": "11,14", "D5S818": "13,13", "D7S82O": "12,12",
                "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
                "D3S1358": "15,16", "D6S1O43": "11,12", "D8S1179": "14,14",
                "Penta E": "12,13", "D1OS1248": "15,15", "D22S1O45": "15,15"}

        form = LocusForm(data)
        if form.is_valid():
            obj = CompareLocusMixin().compare_dnk(form)
            self.assertEqual(len(obj), 2)

    def test_post_found_few_matching_15_locus_1_locus_fail_evrolab(self):
        """
           15 father locus
           22 child locus
        """

        Father.objects.create(name='Tiganis Nicholas',
                              # FGA
                              locus={"FGA": "19,24", "vWA": "16,18", "THO1": "6,9.3",
                                     "TPOX": "8,9", "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
                                     "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
                                     "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "17,24",
                                     "D3S1358": "15,17", "D8S1179": "10,15"})

        Father.objects.create(name='Tiganis Nicholas2',
                              # vWA
                              locus={"FGA": "0,0", "vWA": "5,5", "THO1": "6,9.3",
                                     "TPOX": "8,9", "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
                                     "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
                                     "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "17,24",
                                     "D3S1358": "15,17", "D8S1179": "10,15"})

        data = {
            "FGA": "0,0", "vWA": "16,18", "THO1": "6,9.3",
            "TPOX": "8,9", "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
            "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
            "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "17,24",
            "D3S1358": "15,17", "D8S1179": "10,15",
            # this is unnecessary locus
            'Penta E': "15,17", 'D2S441': "15,17", 'D22S1O45': "15,17",
            'D6S1O43': "15,17", 'D1OS1248': "15,17", 'D1S1656': "15,17",
            'D12S391': "15,17"
        }

        form = LocusForm(data)
        if form.is_valid():
            obj = CompareLocusMixin().compare_dnk(form)
            self.assertEqual(len(obj), 2)

    def test_post_found_few_matching_15_locus_1_locus_fail_mother_and_child(self):
        """
           15 father locus
           15 child locus
        """

        Father.objects.create(name='Nikolic Aleksandar',
                              # FGA
                              locus={"FGA": "1,1", "vWA": "17,18", "THO1": "6,10", "TPOX": "9.10", "CSF1PO": "11.12",
                                     "D18S51": "15,15", "D21S11": "30,31", "D5S818": "11,11", "D7S82O": "9,11",
                                     "D13S317": "11,11", "D16S539": "8,11", "D19S433": "12,13", "D2S1338": "17,17",
                                     "D3S1358": "16,17", "D8S1179": "12,14"})

        Father.objects.create(name='Nikolic Aleksandar2',
                              # vWA
                              locus={"FGA": "0,0", "vWA": "1,1", "THO1": "6,10", "TPOX": "9.10", "CSF1PO": "11.12",
                                     "D18S51": "15,15", "D21S11": "30,31", "D5S818": "11,11", "D7S82O": "9,11",
                                     "D13S317": "11,11", "D16S539": "8,11", "D19S433": "12,13", "D2S1338": "17,17",
                                     "D3S1358": "16,17", "D8S1179": "12,14"})

        data = {"FGA": "0,0", "vWA": "17,18", "THO1": "6,10", "TPOX": "9.10", "CSF1PO": "11.12",
                "D18S51": "15,15", "D21S11": "30,31", "D5S818": "11,11", "D7S82O": "9,11",
                "D13S317": "11,11", "D16S539": "8,11", "D19S433": "12,13", "D2S1338": "17,17",
                "D3S1358": "16,17", "D8S1179": "12,14"}

        form = LocusForm(data)
        if form.is_valid():
            obj = CompareLocusMixin().compare_dnk(form)
            self.assertEqual(len(obj), 2)

    def test_post_found_few_3_matching(self):
        """
           13 father locus
           14 father locus
           12 father locus
           22 child locus
        """

        Father.objects.create(name='Tiganis Nicholas',
                              locus={"vWA": "16,18", "THO1": "6,9.3",
                                     "TPOX": "8,9", "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
                                     "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
                                     "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "17,24",
                                     "D3S1358": "15,17"})

        Father.objects.create(name='Tiganis Nicholas2',
                              locus={"FGA": "0,0", "THO1": "6,9.3",
                                     "TPOX": "8,9", "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
                                     "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
                                     "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "17,24",
                                     "D3S1358": "15,17", "D8S1179": "10,15"})

        Father.objects.create(name='Tiganis Nicholas3',
                              locus={
                                  "TPOX": "8,9", "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
                                  "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
                                  "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "17,24",
                                  "D3S1358": "15,17", "D8S1179": "10,15"
                              })

        data = {
            "FGA": "0,0", "vWA": "16,18", "THO1": "6,9.3",
            "TPOX": "8,9", "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
            "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
            "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "17,24",
            "D3S1358": "15,17", "D8S1179": "10,15",
            # this is unnecessary locus
            'Penta E': "15,17", 'D2S441': "15,17", 'D22S1O45': "15,17",
            'D6S1O43': "15,17", 'D1OS1248': "15,17", 'D1S1656': "15,17",
            'D12S391': "15,17"
        }

        form = LocusForm(data)
        if form.is_valid():
            obj = CompareLocusMixin().compare_dnk(form)
            self.assertEqual(len(obj), 3)

    def test_post_found_few_3_matching_1_locus_failed(self):
        """
           13 father locus
           14 father locus
           12 father locus
           22 child locus
        """

        Father.objects.create(name='Tiganis Nicholas',
                              # D2S1338
                              locus={"vWA": "16,18", "THO1": "6,9.3",
                                     "TPOX": "8,9", "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
                                     "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
                                     "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "0,0",
                                     "D3S1358": "15,17"})

        Father.objects.create(name='Tiganis Nicholas2',
                              # D19S433
                              locus={"FGA": "0,0", "THO1": "6,9.3",
                                     "TPOX": "8,9", "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
                                     "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
                                     "D16S539": "10,11", "D19S433": "0,0", "D2S1338": "17,24",
                                     "D3S1358": "15,17", "D8S1179": "10,15"})

        Father.objects.create(name='Tiganis Nicholas3',
                              locus={
                                  # D5S818
                                  "TPOX": "8,9", "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
                                  "D5S818": "1,1", "D7S82O": "9,12", "D13S317": "11,12",
                                  "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "17,24",
                                  "D3S1358": "15,17", "D8S1179": "10,15"
                              })

        data = {
            "FGA": "0,0", "vWA": "16,18", "THO1": "6,9.3",
            "TPOX": "8,9", "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
            "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
            "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "17,24",
            "D3S1358": "15,17", "D8S1179": "10,15",
            # this is unnecessary locus
            'Penta E': "15,17", 'D2S441': "15,17", 'D22S1O45': "15,17",
            'D6S1O43': "15,17", 'D1OS1248': "15,17", 'D1S1656': "15,17",
            'D12S391': "15,17"
        }

        form = LocusForm(data)
        if form.is_valid():
            obj = CompareLocusMixin().compare_dnk(form)
            self.assertEqual(len(obj), 3)

    def test_post_found_few_not_matching_2_or_more_locus_failed(self):
        """
           13 father locus
           14 father locus
           12 father locus
           22 child locus
        """

        Father.objects.create(name='Tiganis Nicholas',
                              # D2S1338 D19S433
                              locus={"vWA": "16,18", "THO1": "6,9.3",
                                     "TPOX": "8,9", "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
                                     "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
                                     "D16S539": "10,11", "D19S433": "0,0", "D2S1338": "0,0",
                                     "D3S1358": "15,17"})

        Father.objects.create(name='Tiganis Nicholas2',
                              # D19S433 D16S539
                              locus={"FGA": "0,0", "THO1": "6,9.3",
                                     "TPOX": "8,9", "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
                                     "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
                                     "D16S539": "100,111", "D19S433": "0,0", "D2S1338": "17,24",
                                     "D3S1358": "15,17", "D8S1179": "10,15"})

        Father.objects.create(name='Tiganis Nicholas3',
                              locus={
                                  # D5S818 D7S82O
                                  "TPOX": "8,9", "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
                                  "D5S818": "1,1", "D7S82O": "99,112", "D13S317": "11,12",
                                  "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "17,24",
                                  "D3S1358": "15,17", "D8S1179": "10,15"
                              })

        data = {
            "FGA": "0,0", "vWA": "16,18", "THO1": "6,9.3",
            "TPOX": "8,9", "CSF1PO": "12,12", "D18S51": "13,14", "D21S11": "29,31",
            "D5S818": "13,13", "D7S82O": "9,12", "D13S317": "11,12",
            "D16S539": "10,11", "D19S433": "12,14", "D2S1338": "17,24",
            "D3S1358": "15,17", "D8S1179": "10,15",
            # this is unnecessary locus
            'Penta E': "15,17", 'D2S441': "15,17", 'D22S1O45': "15,17",
            'D6S1O43': "15,17", 'D1OS1248': "15,17", 'D1S1656': "15,17",
            'D12S391': "15,17"
        }

        form = LocusForm(data)
        if form.is_valid():
            obj = CompareLocusMixin().compare_dnk(form)
            self.assertEqual(len(obj), 0)
