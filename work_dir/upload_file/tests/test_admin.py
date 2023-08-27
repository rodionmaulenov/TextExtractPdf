# from upload_file.models import Client, Child
# from upload_file.admin import ClientAdmin, ChildCountFilter
#
# from django.test import TestCase
# from django.contrib.admin import site
# from django.test.client import RequestFactory
#
# from unittest.mock import Mock
#
#
# class ChildCountFilterTestCase(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.client_admin = ClientAdmin(Client, site)
#         self.child_count_filter = ChildCountFilter(None, {}, Client, self.client_admin)
#         self.parent1 = Client.objects.create(name="Parent 1")
#         self.parent2 = Client.objects.create(name="Parent 2")
#         self.child1 = Child.objects.create(client=self.parent1)
#         self.child2 = Child.objects.create(client=self.parent2)
#         self.child3 = Child.objects.create(client=self.parent2)
#
#     # def test_lookups(self):
#     #     expected_lookups = [
#     #         ('0', 'zero childs'),
#     #         ('1', 'one childs'),
#     #         ('2', 'two childs'),
#     #         ('3', 'three childs'),
#     #         ('4', 'four childs')
#     #     ]
#     #     lookups = ChildCountFilter.lookups(None, self.client_admin)
#     #     self.assertEqual(lookups, expected_lookups)
#
#     def test_queryset_filter(self):
#         # Create a mock request
#         filter = ChildCountFilter(None, {'childs': str(1)}, Client, self.client_admin)
#         poll = filter.queryset(None, Child.objects.all())
#         print(poll)

