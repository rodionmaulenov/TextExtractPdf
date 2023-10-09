from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group


class FileUploadViewTestCase(TestCase):
    def setUp(self):
        # Create a test user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpassword', is_staff=True)
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_get_authenticated_and_has_groups(self):
        group1 = Group.objects.create(name='users_input_text')
        group2 = Group.objects.create(name='users_upload')
        group1.user_set.add(self.user)
        group2.user_set.add(self.user)

        url = reverse('upload_file')  # Replace with the actual view name

        response = self.client.get(url)

        # Check that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # You can also check for the presence of specific content in the response HTML if needed
        self.assertContains(response, 'Upload Files')

    def test_get_authenticated_without_groups(self):

        url = reverse('upload_file')  # Replace with the actual view name

        response = self.client.get(url)

        # Check that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 403)

        # Check that the response content matches your expected message
        expected_message = "Unauthorized access, you don't have correct credentials"
        self.assertContains(response, expected_message, status_code=403)

    def test_get_superuser(self):
        self.user = User.objects.create_user(username='superuser', password='password', is_superuser=True)
        self.client.login(username='superuser', password='password')

        url = reverse('upload_file')  # Replace with the actual view name

        response = self.client.get(url)

        # Check that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response content matches your expected message
        self.assertContains(response, 'PDF allowed')
