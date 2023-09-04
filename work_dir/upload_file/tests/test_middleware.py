from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class MiddleWearTestCase(TestCase):
    def test_get_request_to_home_url_unauthorized(self):
        url = '/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/admin/")

    def test_get_request_to_home_url_authorized(self):
        user = User.objects.create_user(username='testuser', password='testpassword', is_staff=True)
        self.client.force_login(user)
        url = '/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/admin/")

    def test_none_authenticated_user_get_admin_url(self):
        admin_url = reverse('admin:index')
        response = self.client.get(admin_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/admin/login/?next=/admin/")

    def test_authenticated_user_get_admin_url(self):
        user = User.objects.create_user(username='testuser', password='testpassword', is_staff=True)
        self.client.force_login(user)
        admin_url = reverse('admin:index')
        response = self.client.get(admin_url)

        self.assertEqual(response.status_code, 200)
        print(response.context)
