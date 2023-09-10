from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.messages import get_messages, ERROR
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpRequest
from django.test import TestCase, RequestFactory

from upload_file.admin import ClientAdmin
from upload_file.forms import DnkForm
from upload_file.models import Client, Child
from upload_file.services import verify_data


class MyAdminViewGetRequestTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = '/admin/upload_file/client/form/'

    def test_my_view_get_request_invalid_url_when_authorized_and_have_credentials(self):
        User.objects.create_user(username='staff', password='password', is_staff=True)
        self.client.login(username='staff', password='password')
        response = self.client.get('admin:invalid_url')
        self.assertEqual(response.status_code, 404)

    def test_my_view_get_request_unauthorized_access(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/admin/login/?next=/admin/upload_file/client/form/')

    def test_my_view_get_request_when_authorized_but_has_not_credentials_access(self):
        User.objects.create_user(username='staff', password='password')
        self.client.login(username='staff', password='password')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/admin/login/?next=/admin/upload_file/client/form/')


class MyAdminViewPostRequestUploadFormTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_admin = ClientAdmin(Client, admin.site)
        cls.url = '/admin/upload_file/client/form/'
        cls.pdf_path = 'test_pdf/TasuVasile.pdf'

    def tearDown(self):
        Client.objects.all().delete()

    def setUp(self) -> None:
        self.super_user = User.objects.create_user(username='superuser', password='password', is_staff=True,
                                                   is_superuser=True)
        self.user = User.objects.create_user(username='testuser', password='password', is_staff=True)

        group1 = Group.objects.create(name='user_input_text')
        group2 = Group.objects.create(name='users_upload')
        self.user.groups.add(group1, group2)

        self.client.login(username='testuser', password='password')
        self.client.login(username='superuser', password='password')

    def add_group_to_user(self, user, group_name):
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

    def test_my_view_upload_form_valid_post_request_created_client_instance_view_level_with_group_and_staff_credentials(
            self):
        with open(self.pdf_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        uploaded_file = SimpleUploadedFile('real_file.pdf', pdf_content, content_type='application/pdf')

        data = {
            'upload_form_submit': '',
            'file_upload': uploaded_file
        }

        # Create a request object and set the user attribute
        request = RequestFactory().post(self.url, data)
        request.user = self.user  # Set the user attribute to the logged-in user

        # Add the user to a group
        self.add_group_to_user(request.user, 'user_input_text')
        self.add_group_to_user(request.user, 'users_upload')

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = self.client_admin.my_view(request)

        self.assertEqual(response.status_code, 302)

        self.assertTrue(Client.objects.exists())

        messages = list(get_messages(request))
        message = ''
        for m in messages:
            message += str(m)

        self.assertEqual(message, 'Client instance Tasu Vasile saved successfully')

    def test_my_view_upload_form_valid_post_request_created_client_instance_view_level_if_superuser(self):
        with open(self.pdf_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        uploaded_file = SimpleUploadedFile('real_file.pdf', pdf_content, content_type='application/pdf')

        data = {
            'upload_form_submit': '',
            'file_upload': uploaded_file
        }

        # Create a request object and set the user attribute
        request = RequestFactory().post(self.url, data)
        request.user = self.super_user  # Set the user attribute to the logged-in user

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = self.client_admin.my_view(request)

        self.assertEqual(response.status_code, 302)

        self.assertTrue(Client.objects.exists())

        messages = list(get_messages(request))
        message = ''
        for m in messages:
            message += str(m)

        self.assertEqual(message, 'Client instance Tasu Vasile saved successfully')

    def test_my_view_upload_form_valid_post_request_created_client_instance_with_group_and_staff_credentials(self):
        with open(self.pdf_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        uploaded_file = SimpleUploadedFile('real_file.pdf', pdf_content, content_type='application/pdf')

        data = {
            'upload_form_submit': '',
            'file_upload': uploaded_file
        }

        self.client.login(username='testuser', password='password')
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        self.assertTrue(Client.objects.exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Client instance Tasu Vasile saved successfully')

    def test_my_view_upload_form_valid_post_request_created_client_instance_if_superuser(self):
        with open(self.pdf_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        uploaded_file = SimpleUploadedFile('real_file.pdf', pdf_content, content_type='application/pdf')

        data = {
            'upload_form_submit': '',
            'file_upload': uploaded_file
        }

        self.client.login(username='superuser', password='password')
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        self.assertTrue(Client.objects.exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Client instance Tasu Vasile saved successfully')

    def test_my_view_upload_form_invalid_post_request_created_client_instance_with_group_and_staff_credentials(self):
        data = {
            'upload_form_submit': '',
        }

        self.client.login(username='testuser', password='password')
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(Client.objects.exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Form is not valid. Please check the uploaded file.')

    def test_my_view_upload_form_invalid_post_request_created_client_instance_is_superuser(self):
        data = {
            'upload_form_submit': '',
        }

        self.client.login(username='superuser', password='password')
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(Client.objects.exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Form is not valid. Please check the uploaded file.')

    def test_my_view_upload_form_post_request_not_pdf_format_with_group_and_staff_credentials(self):
        fake_txt_content = b'This is a fake TXT content.'
        uploaded_txt_file = SimpleUploadedFile('fake_file.txt', fake_txt_content, content_type='text/plain')

        data = {
            'upload_form_submit': '',
            'file_upload': uploaded_txt_file
        }

        self.client.login(username='testuser', password='password')
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(Client.objects.exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Wrong type file was uploaded. Must be in PDF format')

    def test_my_view_upload_form_post_request_not_pdf_format_is_superuser(self):
        fake_txt_content = b'This is a fake TXT content.'
        uploaded_txt_file = SimpleUploadedFile('fake_file.txt', fake_txt_content, content_type='text/plain')

        data = {
            'upload_form_submit': '',
            'file_upload': uploaded_txt_file
        }

        self.client.login(username='superuser', password='password')
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(Client.objects.exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Wrong type file was uploaded. Must be in PDF format')

    def test_my_view_upload_form_post_request_pdf_format_without_locus_table_with_group_and_staff_credentials(self):
        fake_pdf_content = b'This is a fake TXT content.'
        uploaded_fake_pdf_file = SimpleUploadedFile('fake_file.pdf', fake_pdf_content, content_type='application/pdf')

        data = {
            'upload_form_submit': '',
            'file_upload': uploaded_fake_pdf_file
        }

        self.client.login(username='testuser', password='password')
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(Client.objects.exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Must be a pdf file with locus table')

    def test_my_view_upload_form_post_request_pdf_format_without_locus_table_is_superuser(self):
        fake_pdf_content = b'This is a fake TXT content.'
        uploaded_fake_pdf_file = SimpleUploadedFile('fake_file.pdf', fake_pdf_content, content_type='application/pdf')

        data = {
            'upload_form_submit': '',
            'file_upload': uploaded_fake_pdf_file
        }

        self.client.login(username='superuser', password='password')
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(Client.objects.exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Must be a pdf file with locus table')

    def test_existing_client_upload_form_post_request_with_group_and_staff_credentials(self):
        self.assertEqual(0, Client.objects.count())
        Client.objects.create(name='Tasu Vasile',
                              locus={"FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                                     "CSF1P0": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
                                     "D2S441": "11,14", "D5S818": "13,13", "D7S820": "12,12",
                                     "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                                     "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
                                     "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
                                     "Penta D": "11,12", "Penta E": "12,13", "D10S1248": "15,15",
                                     "D22S1045": "15,15"})
        self.assertEqual(1, Client.objects.count())

        with open(self.pdf_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        uploaded_file = SimpleUploadedFile('real_file.pdf', pdf_content, content_type='application/pdf')

        data = {
            'upload_form_submit': '',
            'file_upload': uploaded_file
        }

        self.client.login(username='testuser', password='password')
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        self.assertTrue(Client.objects.exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Exactly the same client Tasu Vasile already exists')

    def test_existing_client_upload_form_post_request_is_superuser(self):
        self.assertEqual(0, Client.objects.count())
        Client.objects.create(name='Tasu Vasile',
                              locus={"FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                                     "CSF1P0": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
                                     "D2S441": "11,14", "D5S818": "13,13", "D7S820": "12,12",
                                     "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                                     "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
                                     "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
                                     "Penta D": "11,12", "Penta E": "12,13", "D10S1248": "15,15",
                                     "D22S1045": "15,15"})
        self.assertEqual(1, Client.objects.count())

        with open(self.pdf_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        uploaded_file = SimpleUploadedFile('real_file.pdf', pdf_content, content_type='application/pdf')

        data = {
            'upload_form_submit': '',
            'file_upload': uploaded_file
        }

        self.client.login(username='superuser', password='password')
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        self.assertTrue(Client.objects.exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Exactly the same client Tasu Vasile already exists')


class MyAdminViewPostRequestDnkFormTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = '/admin/upload_file/client/form/'

    def setUp(self) -> None:
        self.child = Child.objects.create()
        self.tatu_vasile = Client.objects.create(name='Tasu Vasile',
                                                 locus={"FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                                                        "CSF1P0": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
                                                        "D2S441": "11,14", "D5S818": "13,13", "D7S820": "12,12",
                                                        "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                                                        "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
                                                        "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
                                                        "Penta D": "11,12", "Penta E": "12,13", "D10S1248": "15,15",
                                                        "D22S1045": "15,15"})

        self.super_user = User.objects.create_user(username='superuser', password='password', is_staff=True,
                                                   is_superuser=True)
        self.user = User.objects.create_user(username='testuser', password='password', is_staff=True)

        group1 = Group.objects.create(name='user_input_text')
        group2 = Group.objects.create(name='users_upload')
        self.user.groups.add(group1, group2)

        self.client.login(username='testuser', password='password')
        self.client.login(username='superuser', password='password')

    def test_valid_dnk_form_with_valid_dnk_data_and_verify_data_func_is_True_with_group_and_staff_credentials(self):
        valid_dnk_data = {"FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                          "CSF1P0": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
                          "D2S441": "11,14", "D5S818": "13,13", "D7S820": "12,12",
                          "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                          "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
                          "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
                          "Penta_D": "11,12", "Penta_E": "12,13", "D10S1248": "15,15",
                          "D22S1045": "15,15"}
        dnk_form = DnkForm(valid_dnk_data)
        self.assertTrue(dnk_form.is_valid())

        request = self.client.post('/fake-url/')  # HttpResponseNotFound
        request.user = self.user
        setattr(request, 'session', self.client.session)
        setattr(request, '_messages', FallbackStorage(request))

        dnk = dnk_form.instance
        dnk.child = self.child
        dnk.save()

        result = verify_data(request, dnk, self.child)
        self.assertTrue(result)

    def test_valid_dnk_form_with_valid_dnk_data_and_verify_data_func_is_True_is_superuser(self):
        valid_dnk_data = {"FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                          "CSF1P0": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
                          "D2S441": "11,14", "D5S818": "13,13", "D7S820": "12,12",
                          "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                          "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
                          "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
                          "Penta_D": "11,12", "Penta_E": "12,13", "D10S1248": "15,15",
                          "D22S1045": "15,15"}
        dnk_form = DnkForm(valid_dnk_data)
        self.assertTrue(dnk_form.is_valid())

        request = self.client.post('/fake-url/')  # HttpResponseNotFound
        request.user = self.super_user
        setattr(request, 'session', self.client.session)
        setattr(request, '_messages', FallbackStorage(request))

        dnk = dnk_form.instance
        dnk.child = self.child
        dnk.save()

        result = verify_data(request, dnk, self.child)
        self.assertTrue(result)

    def test_valid_dnk_form_with_valid_dnk_data_and_verify_data_func_is_can_not_be_empty_with_group_and_staff_credentials(
            self):
        valid_dnk_data = {"FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                          "CSF1P0": "", "D18S51": "13,16", "D21S11": "29,30.2",
                          "D2S441": "11,14", "D5S818": "13,13", "D7S820": "12,12",
                          "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                          "D19S433": "13,13", "D1S1656": "", "D2S1338": "19,20",
                          "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
                          "Penta_D": "11,12", "Penta_E": "12,13", "D10S1248": "15,15",
                          "D22S1045": "15,15"}
        dnk_form = DnkForm(valid_dnk_data)
        self.assertTrue(dnk_form.is_valid())

        request = HttpRequest()  # Use HttpRequest instead of HttpResponseNotFound
        setattr(request, 'session', self.client.session)
        setattr(request, '_messages', FallbackStorage(request))
        request.user = self.user

        dnk = dnk_form.instance
        dnk.child = self.child
        dnk.save()

        result = verify_data(request, dnk, self.child)
        self.assertFalse(result)

        messages = list(get_messages(request))

        # Check for the error message
        error_messages = [message for message in messages if message.level == ERROR]
        self.assertEqual(len(error_messages), 1)  #
        self.assertIn('Form lines can not be a empty', error_messages[0].message)

    def test_valid_dnk_form_with_valid_dnk_data_and_verify_data_func_is_can_not_be_empty_is_superuser(self):
        valid_dnk_data = {"FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                          "CSF1P0": "", "D18S51": "13,16", "D21S11": "29,30.2",
                          "D2S441": "11,14", "D5S818": "13,13", "D7S820": "12,12",
                          "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                          "D19S433": "13,13", "D1S1656": "", "D2S1338": "19,20",
                          "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
                          "Penta_D": "11,12", "Penta_E": "12,13", "D10S1248": "15,15",
                          "D22S1045": "15,15"}
        dnk_form = DnkForm(valid_dnk_data)
        self.assertTrue(dnk_form.is_valid())

        request = HttpRequest()  # Use HttpRequest instead of HttpResponseNotFound
        setattr(request, 'session', self.client.session)
        setattr(request, '_messages', FallbackStorage(request))
        request.user = self.super_user

        dnk = dnk_form.instance
        dnk.child = self.child
        dnk.save()

        result = verify_data(request, dnk, self.child)
        self.assertFalse(result)

        messages = list(get_messages(request))

        # Check for the error message
        error_messages = [message for message in messages if message.level == ERROR]
        self.assertEqual(len(error_messages), 1)  #
        self.assertIn('Form lines can not be a empty', error_messages[0].message)

    def test_valid_dnk_form_with_valid_dnk_data_and_verify_data_func_is_numbers_from_0_9_with_group_and_staff_credentials(
            self):
        valid_dnk_data = {"FGA": "21as,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                          "CSF1P0": "21,22", "D18S51": "13,16", "D21S11": "29,30.2",
                          "D2S441": "%4,14", "D5S818": "&&,13", "D7S820": "12,12",
                          "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                          "D19S433": "13,13", "D1S1656": "21,22", "D2S1338": "19,20",
                          "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
                          "Penta_D": "11,12", "Penta_E": "12,13", "D10S1248": "15,15",
                          "D22S1045": "15,15"}
        dnk_form = DnkForm(valid_dnk_data)
        self.assertTrue(dnk_form.is_valid())

        request = HttpRequest()  # Use HttpRequest instead of HttpResponseNotFound
        setattr(request, 'session', self.client.session)
        setattr(request, '_messages', FallbackStorage(request))
        request.user = self.user

        dnk = dnk_form.instance
        dnk.child = self.child
        dnk.save()

        result = verify_data(request, dnk, self.child)
        self.assertFalse(result)

        messages = list(get_messages(request))

        # Check for the error message
        error_messages = [message for message in messages if message.level == ERROR]
        self.assertEqual(len(error_messages), 1)  #
        self.assertIn('Fields could contain only numbers from 0 to 9 and dot.', error_messages[0].message)

    def test_valid_dnk_form_with_valid_dnk_data_and_verify_data_func_is_numbers_from_0_9_is_superuser(self):
        valid_dnk_data = {"FGA": "21as,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                          "CSF1P0": "21,22", "D18S51": "13,16", "D21S11": "29,30.2",
                          "D2S441": "%4,14", "D5S818": "&&,13", "D7S820": "12,12",
                          "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                          "D19S433": "13,13", "D1S1656": "21,22", "D2S1338": "19,20",
                          "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
                          "Penta_D": "11,12", "Penta_E": "12,13", "D10S1248": "15,15",
                          "D22S1045": "15,15"}
        dnk_form = DnkForm(valid_dnk_data)
        self.assertTrue(dnk_form.is_valid())

        request = HttpRequest()  # Use HttpRequest instead of HttpResponseNotFound
        setattr(request, 'session', self.client.session)
        setattr(request, '_messages', FallbackStorage(request))
        request.user = self.super_user

        dnk = dnk_form.instance
        dnk.child = self.child
        dnk.save()

        result = verify_data(request, dnk, self.child)
        self.assertFalse(result)

        messages = list(get_messages(request))

        # Check for the error message
        error_messages = [message for message in messages if message.level == ERROR]
        self.assertEqual(len(error_messages), 1)  #
        self.assertIn('Fields could contain only numbers from 0 to 9 and dot.', error_messages[0].message)

    def test_valid_dnk_form_with_valid_dnk_data_and_verify_data_func_is_numbers_integer_or_float_with_group_and_staff_credentials(
            self):
        valid_dnk_data = {"FGA": "21.,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                          "CSF1P0": "21,22", "D18S51": "13,16", "D21S11": "29,30.2",
                          "D2S441": "14,14", "D5S818": "&&,13", "D7S820": "12,12",
                          "D12S391": "19.,20", "D13S317": "8,11", "D16S539": "10,11",
                          "D19S433": "13,13", "D1S1656": "21,22", "D2S1338": "19,20",
                          "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
                          "Penta_D": "11,12", "Penta_E": "12,13", "D10S1248": "15,15",
                          "D22S1045": "15,15"}
        dnk_form = DnkForm(valid_dnk_data)
        self.assertTrue(dnk_form.is_valid())

        request = HttpRequest()  # Use HttpRequest instead of HttpResponseNotFound
        setattr(request, 'session', self.client.session)
        setattr(request, '_messages', FallbackStorage(request))
        request.user = self.user

        dnk = dnk_form.instance
        dnk.child = self.child
        dnk.save()

        result = verify_data(request, dnk, self.child)
        self.assertFalse(result)

        messages = list(get_messages(request))

        # Check for the error message
        error_messages = [message for message in messages if message.level == ERROR]
        self.assertEqual(len(error_messages), 1)  #
        self.assertIn('Value must be integer either float.', error_messages[0].message)

    def test_valid_dnk_form_with_valid_dnk_data_and_verify_data_func_is_numbers_integer_or_float_is_superuser(self):
        valid_dnk_data = {"FGA": "21.,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                          "CSF1P0": "21,22", "D18S51": "13,16", "D21S11": "29,30.2",
                          "D2S441": "14,14", "D5S818": "&&,13", "D7S820": "12,12",
                          "D12S391": "19.,20", "D13S317": "8,11", "D16S539": "10,11",
                          "D19S433": "13,13", "D1S1656": "21,22", "D2S1338": "19,20",
                          "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
                          "Penta_D": "11,12", "Penta_E": "12,13", "D10S1248": "15,15",
                          "D22S1045": "15,15"}
        dnk_form = DnkForm(valid_dnk_data)
        self.assertTrue(dnk_form.is_valid())

        request = HttpRequest()  # Use HttpRequest instead of HttpResponseNotFound
        setattr(request, 'session', self.client.session)
        setattr(request, '_messages', FallbackStorage(request))
        request.user = self.super_user

        dnk = dnk_form.instance
        dnk.child = self.child
        dnk.save()

        result = verify_data(request, dnk, self.child)
        self.assertFalse(result)

        messages = list(get_messages(request))

        # Check for the error message
        error_messages = [message for message in messages if message.level == ERROR]
        self.assertEqual(len(error_messages), 1)  #
        self.assertIn('Value must be integer either float.', error_messages[0].message)

    def test_valid_dnk_form_with_valid_dnk_data_and_verify_data_func_is_separated_comma_with_group_and_staff_credentials(
            self):
        valid_dnk_data = {"FGA": "21.22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                          "CSF1P0": "2122", "D18S51": "13,16", "D21S11": "29,30.2",
                          "D2S441": "14,14", "D5S818": "&&,13", "D7S820": "12,12",
                          "D12S391": "19.,20", "D13S317": "8,11", "D16S539": "10,11",
                          "D19S433": "13,13", "D1S1656": "21,22", "D2S1338": "19,20",
                          "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
                          "Penta_D": "11,12", "Penta_E": "12,13", "D10S1248": "15,15",
                          "D22S1045": "15,15"}
        dnk_form = DnkForm(valid_dnk_data)
        self.assertTrue(dnk_form.is_valid())

        request = HttpRequest()  # Use HttpRequest instead of HttpResponseNotFound
        setattr(request, 'session', self.client.session)
        setattr(request, '_messages', FallbackStorage(request))
        request.user = self.user

        dnk = dnk_form.instance
        dnk.child = self.child
        dnk.save()

        result = verify_data(request, dnk, self.child)
        self.assertFalse(result)

        messages = list(get_messages(request))

        # Check for the error message
        error_messages = [message for message in messages if message.level == ERROR]
        self.assertEqual(len(error_messages), 1)  #
        self.assertIn('Numbers must be separated by a comma.', error_messages[0].message)

    def test_view_post_dnk_form_submit_valid_matching_find_is_superuser(self):
        data = {
            'dnk_form_submit': '',
            "FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
            "CSF1P0": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
            "D2S441": "11,14", "D5S818": "13,13", "D7S820": "12,12",
            "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
            "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
            "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
            "Penta_D": "11,12", "Penta_E": "12,13", "D10S1248": "15,15",
            "D22S1045": "15,15"
        }

        request = RequestFactory().post(self.url, data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.super_user

        client_admin = ClientAdmin(Client, admin.site)
        response = client_admin.my_view(request)

        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(request))
        message = ''
        for m in messages:
            message += str(m)

        self.assertEqual(message, 'We have matching father TASU VASILE')

    def test_view_post_dnk_form_submit_valid_matching_not_find_with_group_and_staff_credentials(self):
        data = {
            'dnk_form_submit': '',
            "FGA": "10,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
            "CSF1P0": "5,5", "D18S51": "13,16", "D21S11": "29,30.2",
            "D2S441": "10,13", "D5S818": "13,13", "D7S820": "12,12",
            "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
            "D19S433": "16,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
            "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
            "Penta_D": "11,12", "Penta_E": "12,13", "D10S1248": "15,15",
            "D22S1045": "15,15", 'papa_karlo': 123,
        }

        request = RequestFactory().post(self.url, data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user

        client_admin = ClientAdmin(Client, admin.site)
        response = client_admin.my_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/admin/upload_file/client/form/')

        messages = list(get_messages(request))
        message = ''
        for m in messages:
            message += str(m)

        self.assertEqual(message, 'Matching not found. Maybe you enter invalid data')

    def test_view_post_dnk_form_submit_valid_matching_not_find_is_superuser(self):
        data = {
            'dnk_form_submit': '',
            "FGA": "10,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
            "CSF1P0": "5,5", "D18S51": "13,16", "D21S11": "29,30.2",
            "D2S441": "10,13", "D5S818": "13,13", "D7S820": "12,12",
            "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
            "D19S433": "16,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
            "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
            "Penta_D": "11,12", "Penta_E": "12,13", "D10S1248": "15,15",
            "D22S1045": "15,15", 'papa_karlo': 123,
        }

        request = RequestFactory().post(self.url, data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.super_user

        client_admin = ClientAdmin(Client, admin.site)
        response = client_admin.my_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/admin/upload_file/client/form/')

        messages = list(get_messages(request))
        message = ''
        for m in messages:
            message += str(m)

        self.assertEqual(message, 'Matching not found. Maybe you enter invalid data')


