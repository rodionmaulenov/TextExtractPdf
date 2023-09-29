from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.messages import get_messages, ERROR
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpRequest
from django.test import TestCase, RequestFactory

from upload_file.admin import ClientAdmin
from upload_file.models import Client


class MyAdminViewPostRequestUploadFormTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_admin = ClientAdmin(Client, admin.site)
        cls.url = '/admin/upload_file/client/form/'
        cls.mother_and_child = 'pdf_for_test/mother_and_child.pdf'
        cls.eurolab = 'pdf_for_test/eurolab.pdf'
        cls.brake_logic_pdf_file = 'pdf_for_test/brake_func_logic.pdf'
        cls.file_return_none = 'pdf_for_test/return_none.pdf'

    def tearDown(self):
        Client.objects.all().delete()

    def setUp(self) -> None:
        self.super_user = User.objects.create_user(username='superuser', password='password', is_staff=True,
                                                   is_superuser=True)
        self.user = User.objects.create_user(username='testuser', password='password', is_staff=True)

        group1 = Group.objects.create(name='users_input_text')
        group2 = Group.objects.create(name='users_upload')
        self.user.groups.add(group1, group2)

        self.client.login(username='testuser', password='password')
        self.client.login(username='superuser', password='password')

    def test_mother_and_child_valid_post_request_upload_form_view_level_with_group_and_staff_credentials(self):
        with open(self.mother_and_child, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        uploaded_file = SimpleUploadedFile('real_file.pdf', pdf_content, content_type='application/pdf')

        data = {
            'upload_form_submit': '',
            'file_upload': uploaded_file
        }

        # Create a request object and set the user attribute
        request = RequestFactory().post(self.url, data)
        request.user = self.user  # Set the user attribute to the logged-in user

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

    def test_mother_and_child_valid_post_request_upload_form_view_level_if_superuser(self):
        with open(self.mother_and_child, 'rb') as pdf_file:
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

    def test_evrolab_valid_post_request_upload_form_view_level_with_group_and_staff_credentials(self):
        with open(self.eurolab, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        uploaded_file = SimpleUploadedFile('real_file.pdf', pdf_content, content_type='application/pdf')

        data = {
            'upload_form_submit': '',
            'file_upload': uploaded_file
        }

        # Create a request object and set the user attribute
        request = RequestFactory().post(self.url, data)
        request.user = self.user  # Set the user attribute to the logged-in user

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

        self.assertEqual(message, 'Client instance Tiganis Nicholas saved successfully')

    def test_evrolab_valid_post_request_upload_form_view_level_if_superuser(self):
        with open(self.eurolab, 'rb') as pdf_file:
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

        self.assertEqual(message, 'Client instance Tiganis Nicholas saved successfully')

    #
    def test_post_request_invalid_upload_form_with_group_and_staff_credentials(self):
        data = {
            'upload_form_submit': '',
        }

        self.client.login(username='testuser', password='password')
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(Client.objects.exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Error form. Please check the uploaded file.')

    def test_post_request_invalid_upload_form_is_superuser(self):
        data = {
            'upload_form_submit': '',
        }

        self.client.login(username='superuser', password='password')
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(Client.objects.exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Error form. Please check the uploaded file.')

    def test_post_request_upload_form_not_pdf_format_with_group_and_staff_credentials(self):
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
        self.assertEqual(str(messages[0]), 'Only pdf extension')

    def test_post_request_upload_form_not_pdf_format_is_superuser(self):
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
        self.assertEqual(str(messages[0]), 'Only pdf extension')

    def test_request_post_upload_form_another_pdf_file_broke_func_logic_with_group_and_staff_credentials(self):
        with open(self.brake_logic_pdf_file, 'rb') as pdf_file:
            brake_logic_file = pdf_file.read()

        uploaded_brake_logic_pdf_file = SimpleUploadedFile('fake_file.pdf', brake_logic_file,
                                                           content_type='application/pdf')

        data = {
            'upload_form_submit': '',
            'file_upload': uploaded_brake_logic_pdf_file
        }

        self.client.login(username='testuser', password='password')
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(Client.objects.exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid file')

    def test_request_post_upload_form_another_pdf_file_broke_func_logic_is_superuser(self):
        with open(self.brake_logic_pdf_file, 'rb') as pdf_file:
            brake_logic_file = pdf_file.read()

        uploaded_brake_logic_pdf_file = SimpleUploadedFile('fake_file.pdf', brake_logic_file,
                                                           content_type='application/pdf')

        data = {
            'upload_form_submit': '',
            'file_upload': uploaded_brake_logic_pdf_file
        }

        self.client.login(username='superuser', password='password')
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(Client.objects.exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid file')

    def test_request_post_upload_form_another_pdf_file_return_none_func_logic_with_group_and_staff_credentials(self):
        with open(self.file_return_none, 'rb') as pdf_file:
            brake_logic_file = pdf_file.read()

        uploaded_brake_logic_pdf_file = SimpleUploadedFile('fake_file.pdf', brake_logic_file,
                                                           content_type='application/pdf')

        data = {
            'upload_form_submit': '',
            'file_upload': uploaded_brake_logic_pdf_file
        }

        self.client.login(username='testuser', password='password')
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(Client.objects.exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Return None. Blank file')

    def test_request_post_upload_form_another_pdf_file_return_none_func_logic_is_superuser(self):
        with open(self.file_return_none, 'rb') as pdf_file:
            brake_logic_file = pdf_file.read()

        uploaded_brake_logic_pdf_file = SimpleUploadedFile('fake_file.pdf', brake_logic_file,
                                                           content_type='application/pdf')

        data = {
            'upload_form_submit': '',
            'file_upload': uploaded_brake_logic_pdf_file
        }

        self.client.login(username='superuser', password='password')
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(Client.objects.exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Return None. Blank file')

    def test_mother_and_child_post_request_upload_form_existing_client_with_group_and_staff_credentials(self):
        self.assertEqual(0, Client.objects.count())
        Client.objects.create(name='Tasu Vasile',
                              locus={'D3S1358': '15,16', 'vWA': '16,19', 'D16S539': '10,11', 'CSF1PO': '11,14',
                                     'TPOX': '8,8', 'D8S1179': '14,14', 'D21S11': '29,30.2', 'D18S51': '13,16',
                                     'Penta E': '12,13', 'D2S441': '11,14', 'D19S433': '13,13', 'THO1': '8,9',
                                     'FGA': '21,22', 'D22S1O45': '15,15', 'D5S818': '13,13', 'D13S317': '8,11',
                                     'D7S82O': '12,12', 'D6S1O43': '11,12', 'D1OS1248': '15,15', 'D1S1656': '14,16.3',
                                     'D12S391': '19,20', 'D2S1338': '19,20', 'Penta D': '11,12'}
                              )
        self.assertEqual(1, Client.objects.count())

        with open(self.mother_and_child, 'rb') as pdf_file:
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

    def test_mother_and_child_post_request_upload_form_existing_client_is_superuser(self):
        self.assertEqual(0, Client.objects.count())
        Client.objects.create(name='Tasu Vasile',
                              locus={'D3S1358': '15,16', 'vWA': '16,19', 'D16S539': '10,11', 'CSF1PO': '11,14',
                                     'TPOX': '8,8', 'D8S1179': '14,14', 'D21S11': '29,30.2', 'D18S51': '13,16',
                                     'Penta E': '12,13', 'D2S441': '11,14', 'D19S433': '13,13', 'THO1': '8,9',
                                     'FGA': '21,22', 'D22S1O45': '15,15', 'D5S818': '13,13', 'D13S317': '8,11',
                                     'D7S82O': '12,12', 'D6S1O43': '11,12', 'D1OS1248': '15,15', 'D1S1656': '14,16.3',
                                     'D12S391': '19,20', 'D2S1338': '19,20', 'Penta D': '11,12'}

                              )

        locus_from_mother_and_child = ['D3S1358', 'vWA', 'D16S539', 'CSF1PO', 'TPOX', 'D8S1179', 'D21S11', 'D18S51',
                                       'Penta E',
                                       'D2S441', 'D19S433', 'THO1', 'FGA', 'D22S1045', 'D5S818', 'D13S317', 'D7S820',
                                       'D6S1043',
                                       'D10S1248', 'D1S1656', 'D12S391', 'D2S1338', 'Penta D']
        self.assertEqual(1, Client.objects.count())

        with open(self.mother_and_child, 'rb') as pdf_file:
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

    def test_eurolab_post_request_upload_form_existing_client_with_group_and_staff_credentials(self):
        self.assertEqual(0, Client.objects.count())
        Client.objects.create(name='Tiganis Nicholas',
                              locus={'D8S1179': '10,15', 'D21S11': '29,31', 'D7S82O': '9,12', 'CSF1PO': '12,12',
                                     'D3S1358': '15,17', 'THO1': '6,9.3', 'D13S317': '11,12', 'D16S539': '10,11',
                                     'D2S1338': '17,24', 'D19S433': '12,14', 'vWA': '16,18', 'TPOX': '8,9',
                                     'D18S51': '13,14', 'D5S818': '13,13', 'FGA': '19,24'}
                              )

        self.assertEqual(1, Client.objects.count())

        with open(self.eurolab, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        uploaded_file = SimpleUploadedFile('real_file.pdf', pdf_content, content_type='application/pdf')

        data = {
            'upload_form_submit': '',
            'file_upload': uploaded_file
        }

        self.client.login(username='testuser', password='password')
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Exactly the same client Tiganis Nicholas already exists')

    def test_eurolab_post_request_upload_form_existing_client_is_superuser(self):
        self.assertEqual(0, Client.objects.count())
        Client.objects.create(name='Tiganis Nicholas',
                              locus={'D8S1179': '10,15', 'D21S11': '29,31', 'D7S82O': '9,12', 'CSF1PO': '12,12',
                                     'D3S1358': '15,17', 'THO1': '6,9.3', 'D13S317': '11,12', 'D16S539': '10,11',
                                     'D2S1338': '17,24', 'D19S433': '12,14', 'vWA': '16,18', 'TPOX': '8,9',
                                     'D18S51': '13,14', 'D5S818': '13,13', 'FGA': '19,24'}
                              )

        self.assertEqual(1, Client.objects.count())

        with open(self.eurolab, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        uploaded_file = SimpleUploadedFile('real_file.pdf', pdf_content, content_type='application/pdf')

        data = {
            'upload_form_submit': '',
            'file_upload': uploaded_file
        }

        self.client.login(username='superuser', password='password')
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Exactly the same client Tiganis Nicholas already exists')
