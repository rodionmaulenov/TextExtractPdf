from django.test import TestCase
from django.contrib.auth.models import User, Group


class TestUserInGroupDecorator(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = '/admin/upload_file/client/form/'

    def test_user_in_correct_group(self):
        user = User.objects.create_user(username='testuser', password='password', is_staff=True)
        group1 = Group.objects.create(name='users_input_text')
        group2 = Group.objects.create(name='users_upload')
        user.groups.add(group1, group2)

        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/custom_base.html')

    def test_user_not_in_correct_group(self):
        user = User.objects.create_user(username='testuser', password='password', is_staff=True)
        group1 = Group.objects.create(name='other_group')
        group2 = Group.objects.create(name='another_group')
        user.groups.add(group1, group2)

        self.client.force_login(user=user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Unauthorized access, you don`t have correct credentials')

    def test_user_is_super_user(self):
        user = User.objects.create_user(username='testuser', password='password', is_staff=True, is_superuser=True)

        self.client.force_login(user=user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/custom_base.html')

