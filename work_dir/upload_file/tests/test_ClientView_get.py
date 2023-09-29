from django.contrib.auth.models import User
from django.test import TestCase


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