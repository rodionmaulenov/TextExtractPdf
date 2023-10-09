from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group


class InputTextViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', is_staff=True)
        self.client = Client()

    def test_get_authenticated_and_has_groups(self):
        group1 = Group.objects.create(name='users_input_text')
        group2 = Group.objects.create(name='users_upload')
        group1.user_set.add(self.user)
        group2.user_set.add(self.user)
        self.client.login(username='testuser', password='testpassword')

        url = reverse('input_text')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_get_authenticated_without_groups(self):

        url = reverse('input_text')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

        expected_message = "Unauthorized access, you don't have correct credentials"
        self.assertContains(response, expected_message, status_code=403)

    def test_get_superuser(self):
        self.user = User.objects.create_user(username='superuser', password='password', is_superuser=True)
        self.client.login(username='superuser', password='password')

        url = reverse('input_text')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


