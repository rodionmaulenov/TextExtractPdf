# from django.test import TestCase
# from django.core.files.uploadedfile import SimpleUploadedFile
#
# from upload_file.models import Client
# from upload_file.services import ProcessUploadedFile, PdfPlumberMotherAndChild, AwsEvrolab, AwsMotherAndChild
#
# LOCUS = ['D3S1358', 'vWA', 'D16S539', 'CSF1PO', 'TPOX', 'D8S1179', 'D21S11', 'D18S51', 'Penta E',
#          'D2S441', 'D19S433', 'THO1', 'FGA', 'D22S1O45', 'D5S818', 'D13S317', 'D7S82O', 'D6S1O43',
#          'D1OS1248', 'D1S1656', 'D12S391', 'D2S1338']
#
#
# class ProcessUploadedFileMixinTestCase(TestCase):
#     def setUp(self):
#         self.mixin = ProcessUploadedFile
#         self.uploaded_files = []
#
#     def tearDown(self):
#         Client.objects.all().delete()
#
#     def test_process_uploaded_file_success(self):
#         """
#         Mother and child pdf file using in this test
#         """
#
#         with open('upload_file/test_pdf/mother_and_child.pdf', 'rb') as pdf_file:
#             uploaded_file = SimpleUploadedFile(
#                 name='success.pdf',
#                 content=pdf_file.read(),
#                 content_type='application/pdf',
#             )
#
#         list_instance = [AwsEvrolab, PdfPlumberMotherAndChild, AwsMotherAndChild]
#         response = self.mixin(uploaded_file, list_instance).get_message_response()
#
#         expected_response = {'log': 'success', 'message': 'Father Tasu Vasile saved successfully'}
#         self.assertEqual(response, expected_response)
#         self.assertEqual(Client.objects.count(), 1)
#
#     def test_process_uploaded_file_already_exists(self):
#         """
#         Mother and child pdf file using in this test
#         """
#
#         Client.objects.create(
#             name='Tasu Vasile',
#             locus={'D3S1358': '15,16', 'vWA': '16,19', 'D16S539': '10,11', 'CSF1PO': '11,14', 'TPOX': '8,8',
#                    'D8S1179': '14,14', 'D21S11': '29,30.2', 'D18S51': '13,16', 'Penta E': '12,13', 'D2S441': '11,14',
#                    'D19S433': '13,13', 'THO1': '8,9', 'FGA': '21,22', 'D22S1O45': '15,15', 'D5S818': '13,13',
#                    'D13S317': '8,11', 'D7S82O': '12,12', 'D6S1O43': '11,12', 'D1OS1248': '15,15', 'D1S1656': '14,16.3',
#                    'D12S391': '19,20', 'D2S1338': '19,20'}
#         )
#
#         with open('upload_file/test_pdf/mother_and_child.pdf', 'rb') as pdf_file:
#             uploaded_file = SimpleUploadedFile(
#                 name='success.pdf',
#                 content=pdf_file.read(),
#                 content_type='application/pdf',
#             )
#
#         list_instance = [AwsEvrolab, PdfPlumberMotherAndChild, AwsMotherAndChild]
#         response = self.mixin(uploaded_file, list_instance).get_message_response()
#
#         expected_response = {'log': 'caution', 'message': 'Father Tasu Vasile already exists'}
#         self.assertEqual(response, expected_response)
#         self.assertEqual(Client.objects.count(), 1)
#
#     def test_process_uploaded_file_success_eurolab(self):
#         """
#         Eurolab pdf file using in this test
#         """
#
#         with open('upload_file/test_pdf/eurolab.pdf', 'rb') as pdf_file:
#             uploaded_file = SimpleUploadedFile(
#                 name='success.pdf',
#                 content=pdf_file.read(),
#                 content_type='application/pdf',
#             )
#
#         list_instance = [AwsEvrolab, PdfPlumberMotherAndChild, AwsMotherAndChild]
#         response = self.mixin(uploaded_file, list_instance).get_message_response()
#
#         expected_response = {'log': 'success', 'message': 'Father Tiganis Nicholas saved successfully'}
#         self.assertEqual(response, expected_response)
#         self.assertEqual(Client.objects.count(), 1)
#
#     def test_process_uploaded_file_already_exists_eurolab(self):
#         """
#         Eurolab pdf file using in this test
#         """
#
#         Client.objects.create(
#             name='Tiganis Nicholas',
#             locus={'D8S1179': '10,15', 'D21S11': '29,31', 'D7S82O': '9,12', 'CSF1PO': '12,12', 'D3S1358': '15,17',
#                    'THO1': '6,9.3', 'D13S317': '11,12', 'D16S539': '10,11', 'D2S1338': '17,24', 'D19S433': '12,14',
#                    'vWA': '16,18', 'TPOX': '8,9', 'D18S51': '13,14', 'D5S818': '13,13', 'FGA': '19,24'}
#         )
#
#         with open('upload_file/test_pdf/eurolab.pdf', 'rb') as pdf_file:
#             uploaded_file = SimpleUploadedFile(
#                 name='success.pdf',
#                 content=pdf_file.read(),
#                 content_type='application/pdf',
#
#             )
#
#         list_instance = [AwsEvrolab, PdfPlumberMotherAndChild, AwsMotherAndChild]
#         response = self.mixin(uploaded_file, list_instance).get_message_response()
#
#         expected_response = {'log': 'caution', 'message': 'Father Tiganis Nicholas already exists'}
#         self.assertEqual(response, expected_response)
#         self.assertEqual(Client.objects.count(), 1)
#
#     def test_process_uploaded_file_fail_1(self):
#         with open('upload_file/test_pdf/return_none.pdf', 'rb') as pdf_file:
#             uploaded_file = SimpleUploadedFile(
#                 name='success.pdf',
#                 content=pdf_file.read(),
#                 content_type='application/pdf',
#             )
#
#         list_instance = [AwsEvrolab, PdfPlumberMotherAndChild, AwsMotherAndChild]
#         response = self.mixin(uploaded_file, list_instance).get_message_response()
#
#         expected_response = {'log': 'error', 'message': 'Error processing'}
#         self.assertEqual(response, expected_response)
#         self.assertEqual(Client.objects.count(), 0)
#
#     def test_process_uploaded_file_fail_2(self):
#         with open('upload_file/test_pdf/brake_func_logic.pdf', 'rb') as pdf_file:
#             uploaded_file = SimpleUploadedFile(
#                 name='success.pdf',
#                 content=pdf_file.read(),
#                 content_type='application/pdf',
#             )
#
#         list_instance = [AwsEvrolab, PdfPlumberMotherAndChild, AwsMotherAndChild]
#         response = self.mixin(uploaded_file, list_instance).get_message_response()
#
#         expected_response = {'log': 'error', 'message': 'Error processing'}
#         self.assertEqual(response, expected_response)
#         self.assertEqual(Client.objects.count(), 0)
#
#     def test_process_uploaded_file_success_aws_MAC_15(self):
#         """
#         MotherAndChild pdf file
#         15 locus
#         """
#
#         with open('upload_file/test_pdf/Nikolic Aleksandar.pdf', 'rb') as pdf_file:
#             uploaded_file = SimpleUploadedFile(
#                 name='success.pdf',
#                 content=pdf_file.read(),
#                 content_type='application/pdf',
#             )
#
#         list_instance = [AwsEvrolab, PdfPlumberMotherAndChild, AwsMotherAndChild]
#         response = self.mixin(uploaded_file, list_instance).get_message_response()
#
#         expected_response = {'log': 'success', 'message': 'Father Nikolic Aleksandar saved successfully'}
#         self.assertEqual(response, expected_response)
#         self.assertEqual(Client.objects.count(), 1)
#
#     def test_process_uploaded_file_already_exists_aws_MAC_15(self):
#         """
#         MotherAndChild pdf file
#         15 locus
#         """
#
#         Client.objects.create(
#             name='Nikolic Aleksandar',
#             locus={"FGA": "21,21", "vWA": "17,18", "THO1": "6,10", "TPOX": "9.10", "CSF1PO": "11.12", "D18S51": "15,15",
#                    "D21S11": "30,31", "D5S818": "11,11", "D7S82O": "9,11", "D13S317": "11,11", "D16S539": "8,11",
#                    "D19S433": "12,13", "D2S1338": "17,17", "D3S1358": "16,17", "D8S1179": "12,14"}
#         )
#
#         with open('upload_file/test_pdf/Nikolic Aleksandar.pdf', 'rb') as pdf_file:
#             uploaded_file = SimpleUploadedFile(
#                 name='success.pdf',
#                 content=pdf_file.read(),
#                 content_type='application/pdf',
#
#             )
#
#         list_instance = [AwsEvrolab, PdfPlumberMotherAndChild, AwsMotherAndChild]
#         response = self.mixin(uploaded_file, list_instance).get_message_response()
#
#         expected_response = {'log': 'caution', 'message': 'Father Nikolic Aleksandar already exists'}
#         self.assertEqual(response, expected_response)
#         self.assertEqual(Client.objects.count(), 1)
#
#     def test_process_uploaded_file_success_aws_MAC_22_name_rus(self):
#         """
#         MotherAndChild pdf file
#         22 locus
#         name file on rus
#         """
#
#         with open('upload_file/test_pdf/Даніель Фаріаш Гомес.pdf', 'rb') as pdf_file:
#             uploaded_file = SimpleUploadedFile(
#                 name='success.pdf',
#                 content=pdf_file.read(),
#                 content_type='application/pdf',
#             )
#
#         list_instance = [AwsEvrolab, PdfPlumberMotherAndChild, AwsMotherAndChild]
#         response = self.mixin(uploaded_file, list_instance).get_message_response()
#
#         expected_response = {'log': 'success', 'message': 'Father success saved successfully'}
#         self.assertEqual(response, expected_response)
#         self.assertEqual(Client.objects.count(), 1)
#
#     def test_process_uploaded_file_already_exists_aws_MAC_22_name_rus(self):
#         """
#         MotherAndChild pdf file
#         22 locus
#         name file on rus
#         """
#
#         Client.objects.create(
#             name='Даніель Фаріаш Гомес',
#             locus={"FGA": "23,25", "vWA": "16,18", "THO1": "6,8", "TPOX": "8,11", "CSF1PO": "10,12", "D18S51": "13,19",
#                    "D21S11": "30,32.2", "D2S441": "11,14", "D5S818": "12,12", "D7S82O": "8,10", "D12S391": "20,21",
#                    "D13S317": "11,12", "D16S539": "12,14", "D19S433": "15.2,16", "D1S1656": "14,14", "D2S1338": "19,24",
#                    "D3S1358": "16,16", "D6S1O43": "11,12", "D8S1179": "13,15", "Penta E": "7,11", "D1OS1248": "14,16",
#                    "D22S1O45": "11,17"}
#         )
#
#         with open('upload_file/test_pdf/Даніель Фаріаш Гомес.pdf', 'rb') as pdf_file:
#             uploaded_file = SimpleUploadedFile(
#                 name='Даніель Фаріаш Гомес.pdf',
#                 content=pdf_file.read(),
#                 content_type='application/pdf',
#
#             )
#
#         list_instance = [AwsEvrolab, PdfPlumberMotherAndChild, AwsMotherAndChild]
#         response = self.mixin(uploaded_file, list_instance).get_message_response()
#
#         expected_response = {'log': 'caution', 'message': 'Father Даніель Фаріаш Гомес already exists'}
#         self.assertEqual(response, expected_response)
#         self.assertEqual(Client.objects.count(), 1)
