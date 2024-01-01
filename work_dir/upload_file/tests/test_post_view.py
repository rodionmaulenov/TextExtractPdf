from unittest.mock import patch, MagicMock

from django.core.files.base import ContentFile
from django.test import TransactionTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile

from upload_file.models import Client
from upload_file.test_pdf.evrolab import evrolab_dict_for_locus, evrolab_dict_for_name
from upload_file.test_pdf.fail import fail
from upload_file.test_pdf.mother_and_child_15 import locus_dict_15
from upload_file.test_pdf.mother_and_child_22 import mother_and_child_dict
from upload_file.test_pdf.mother_and_child_22_name_on_rus import locus_dict_22_on_rus
from upload_file.services import ProcessUploadedFile, AwsEvrolab, AwsMotherAndChild, \
    AwsMotherAndChildV2, AwsMotherAndChildV3, AwsEvrolabV2

Client: models


class ProcessUploadedFileMixinTestCase(TransactionTestCase):
    def setUp(self):
        self.mixin = ProcessUploadedFile
        self.uploaded_files = []

    def tearDown(self):
        Client.objects.all().delete()

    @patch('upload_file.services.boto3.client')
    def test_process_uploaded_file_success(self, boto_client_mock):
        """
        MotherAndChild pdf file on 2 page
        22 locus
        :return: message Response
        """
        # connect to aws with client credentials
        mock_textract = MagicMock()
        boto_client_mock.return_value = mock_textract

        # return dict
        # in this case analyze_text with TABLES format
        mock_textract.analyze_document.return_value = mother_and_child_dict

        with open('upload_file/test_pdf/mother_and_child_22.pdf', 'rb') as pdf_file:
            uploaded_file = SimpleUploadedFile(
                name='success.pdf',
                content=pdf_file.read(),
                content_type='application/pdf',
            )

        list_instance = [
            AwsMotherAndChildV2
        ]
        instance = self.mixin(uploaded_file, list_instance, 'media_jpg')
        father_dict = instance.process_file()
        response = instance.message_response(father_dict)
        instance.clean_folder()

        expected_response = {'log': 'success', 'message': 'Tasu Vasile saved successfully'}
        self.assertEqual(response, expected_response)
        self.assertEqual(Client.objects.count(), 1)

    @patch('upload_file.services.boto3.client')
    def test_process_uploaded_file_already_exists(self, boto_client_mock):
        """
        MotherAndChild pdf file on 2 page
        22 locus
        :return: message Response
        """

        # connect to aws with client credentials
        mock_textract = MagicMock()
        boto_client_mock.return_value = mock_textract

        # return dict
        # in this case analyze_text with TABLES format
        mock_textract.analyze_document.return_value = mother_and_child_dict

        Client.objects.create(
            name='Tasu Vasile',
            locus={'D3S1358': '15,16', 'vWA': '16,19', 'D16S539': '10,11', 'CSF1PO': '11,14', 'TPOX': '8,8',
                   'D8S1179': '14,14', 'D21S11': '29,30.2', 'D18S51': '13,16', 'Penta E': '12,13', 'D2S441': '11,14',
                   'D19S433': '13,13', 'THO1': '8,9', 'FGA': '21,22', 'D22S1O45': '15,15', 'D5S818': '13,13',
                   'D13S317': '8,11', 'D7S82O': '12,12', 'D6S1O43': '11,12', 'D1OS1248': '15,15', 'D1S1656': '14,16.3',
                   'D12S391': '19,20', 'D2S1338': '19,20'}
        )

        with open('upload_file/test_pdf/mother_and_child_22.pdf', 'rb') as pdf_file:
            uploaded_file = SimpleUploadedFile(
                name='success.pdf',
                content=pdf_file.read(),
                content_type='application/pdf',
            )

        list_instance = [
            AwsMotherAndChildV2
        ]
        instance = self.mixin(uploaded_file, list_instance, 'media_jpg')
        father_dict = instance.process_file()
        response = instance.message_response(father_dict)
        instance.clean_folder()

        expected_response = {'log': 'caution', 'message': 'Tasu Vasile already exists'}
        self.assertEqual(response, expected_response)
        self.assertEqual(Client.objects.count(), 1)

    @patch('upload_file.services.boto3.client')
    def test_process_uploaded_file_success_eurolab(self, boto_client_mock):
        """
        Eurolab pdf file using in this test
        15 locus
        0 page
        """
        dict_for_locus = evrolab_dict_for_locus
        dict_for_name = evrolab_dict_for_name

        mock_textract = MagicMock()

        # return dict
        # in this case repeat analyze with Form format
        mock_textract.analyze_document.side_effect = [dict_for_locus, dict_for_name]

        # connect to aws with client credentials
        boto_client_mock.return_value = mock_textract

        with open('upload_file/test_pdf/eurolab.pdf', 'rb') as pdf_file:
            uploaded_file = SimpleUploadedFile(
                name='success.pdf',
                content=pdf_file.read(),
                content_type='application/pdf',
            )

        list_instance = [
            AwsEvrolab, AwsEvrolabV2
        ]
        instance = self.mixin(uploaded_file, list_instance, 'media_jpg')
        father_dict = instance.process_file()
        response = instance.message_response(father_dict)
        instance.clean_folder()

        expected_response = {'log': 'success', 'message': 'Tiganis Nicholas saved successfully'}
        self.assertEqual(response, expected_response)
        self.assertEqual(Client.objects.count(), 1)

    @patch('upload_file.services.boto3.client')
    def test_process_uploaded_file_already_exists_eurolab(self, boto_client_mock):
        """
        Eurolab pdf file using in this test
        15 locus
        only 0 page
        """

        dict_for_locus = evrolab_dict_for_locus
        dict_for_name = evrolab_dict_for_name

        mock_textract = MagicMock()
        # return dict
        # in this case repeat analyze with Form format
        mock_textract.analyze_document.side_effect = [dict_for_locus, dict_for_name]

        # connect to aws with client credentials
        boto_client_mock.return_value = mock_textract

        Client.objects.create(
            name='Tiganis Nicholas',
            locus={'D8S1179': '10,15', 'D21S11': '29,31', 'D7S82O': '9,12', 'CSF1PO': '12,12', 'D3S1358': '15,17',
                   'THO1': '6,9.3', 'D13S317': '11,12', 'D16S539': '10,11', 'D2S1338': '17,24', 'D19S433': '12,14',
                   'vWA': '16,18', 'TPOX': '8,9', 'D18S51': '13,14', 'D5S818': '13,13', 'FGA': '19,24'}
        )

        with open('upload_file/test_pdf/eurolab.pdf', 'rb') as pdf_file:
            uploaded_file = SimpleUploadedFile(
                name='success.pdf',
                content=pdf_file.read(),
                content_type='application/pdf',

            )

        list_instance = [
            AwsEvrolab
        ]
        instance = self.mixin(uploaded_file, list_instance, 'media_jpg')
        father_dict = instance.process_file()
        response = instance.message_response(father_dict)
        instance.clean_folder()

        expected_response = {'log': 'caution', 'message': 'Tiganis Nicholas already exists'}
        self.assertEqual(response, expected_response)
        self.assertEqual(Client.objects.count(), 1)

    @patch('upload_file.services.boto3.client')
    def test_process_uploaded_file_fail(self, boto_client_mock):
        """
        This file does not have table with locus
        """

        mock_textract = MagicMock()
        # in this case analyze_text with TABLES format
        mock_textract.analyze_document.return_value = mock_textract

        # connect to aws with client credentials
        boto_client_mock.return_value = fail

        with open('upload_file/test_pdf/fail.pdf', 'rb') as pdf_file:
            uploaded_file = SimpleUploadedFile(
                name='success.pdf',
                content=pdf_file.read(),
                content_type='application/pdf',
            )

        list_instance = [
            AwsEvrolab, AwsEvrolabV2,
            AwsMotherAndChild, AwsMotherAndChildV2, AwsMotherAndChildV3
        ]
        instance = self.mixin(uploaded_file, list_instance, 'media_jpg')
        father_dict = instance.process_file()
        response = instance.message_response(father_dict)
        instance.clean_folder()

        expected_response = {'log': 'error', 'message': 'Error processing file'}
        self.assertEqual(response, expected_response)
        self.assertEqual(Client.objects.count(), 0)

    @patch('upload_file.services.boto3.client')
    def test_process_uploaded_file_success_aws_MAC_15(self, boto_client_mock):
        """
        MotherAndChild pdf file on 0 page
        only 15 locus
        """
        mock_textract = MagicMock()
        # in this case analyze_text with TABLES format
        mock_textract.analyze_document.return_value = locus_dict_15

        # connect to aws with client credentials
        boto_client_mock.return_value = mock_textract

        with open('upload_file/test_pdf/mother_and_child_15.pdf', 'rb') as pdf_file:
            uploaded_file = SimpleUploadedFile(
                name='success.pdf',
                content=pdf_file.read(),
                content_type='application/pdf',
            )

        list_instance = [
            AwsMotherAndChild
        ]
        instance = self.mixin(uploaded_file, list_instance, 'media_jpg')
        father_dict = instance.process_file()
        response = instance.message_response(father_dict)
        instance.clean_folder()

        expected_response = {'log': 'success', 'message': 'Nikolic Aleksandar saved successfully'}
        self.assertEqual(response, expected_response)
        self.assertEqual(Client.objects.count(), 1)

    @patch('upload_file.services.boto3.client')
    def test_process_uploaded_file_already_exists_aws_MAC_15(self, boto_client_mock):
        """
        MotherAndChild pdf file on 1 page
        only 15 locus
        :return: message Response
        """

        mock_textract = MagicMock()
        # in this case analyze_text with TABLES format
        mock_textract.analyze_document.return_value = locus_dict_15

        # connect to aws with client credentials
        boto_client_mock.return_value = mock_textract

        Client.objects.create(
            name='Nikolic Aleksandar',
            locus={"FGA": "21,21", "vWA": "17,18", "THO1": "6,10", "TPOX": "9,10", "CSF1PO": "11,12", "D18S51": "15,15",
                   "D21S11": "30,31", "D5S818": "11,11", "D7S82O": "9,11", "D13S317": "11,11", "D16S539": "8,11",
                   "D19S433": "12,13", "D2S1338": "17,17", "D3S1358": "16,17", "D8S1179": "12,14"}
        )

        with open('upload_file/test_pdf/mother_and_child_15.pdf', 'rb') as pdf_file:
            uploaded_file = SimpleUploadedFile(
                name='success.pdf',
                content=pdf_file.read(),
                content_type='application/pdf',

            )

        list_instance = [
            AwsMotherAndChild
        ]
        instance = self.mixin(uploaded_file, list_instance, 'media_jpg')
        father_dict = instance.process_file()
        response = instance.message_response(father_dict)
        instance.clean_folder()
        expected_response = {'log': 'caution', 'message': 'Nikolic Aleksandar already exists'}
        self.assertEqual(response, expected_response)
        self.assertEqual(Client.objects.count(), 1)

    @patch('upload_file.services.boto3.client')
    def test_process_uploaded_file_success_aws_MAC_22_name_rus(self, boto_client_mock):
        """
        MotherAndChild pdf file 1 page
        22 locus
        name file on rus
        """

        mock_textract = MagicMock()
        # in this case analyze_text with TABLES format
        mock_textract.analyze_document.return_value = locus_dict_22_on_rus

        # connect to aws with client credentials
        boto_client_mock.return_value = mock_textract

        with open('upload_file/test_pdf/mother_and_child_22_name_on_rus.pdf', 'rb') as pdf_file:
            uploaded_file = SimpleUploadedFile(
                name='Даніель Фаріаш Гомес.pdf',
                content=pdf_file.read(),
                content_type='application/pdf',
            )

        list_instance = [
            AwsMotherAndChild, AwsMotherAndChildV3, AwsMotherAndChildV2
        ]
        instance = self.mixin(uploaded_file, list_instance, 'media_jpg')
        father_dict = instance.process_file()
        response = instance.message_response(father_dict)
        instance.clean_folder()

        expected_response = {'log': 'success', 'message': 'Даніель Фаріаш Гомес saved successfully'}
        self.assertEqual(response, expected_response)
        self.assertEqual(Client.objects.count(), 1)

    @patch('upload_file.services.boto3.client')
    def test_process_uploaded_file_already_exists_aws_MAC_22_name_rus(self, boto_client_mock):
        """
        MotherAndChild pdf file 1 page
        22 locus
        name file on rus
        :return: message Response
        """

        mock_textract = MagicMock()
        # in this case analyze_text with TABLES format
        mock_textract.analyze_document.return_value = locus_dict_22_on_rus

        # connect to aws with client credentials
        boto_client_mock.return_value = mock_textract

        Client.objects.create(
            name='Даніель Фаріаш Гомес',
            locus={"FGA": "23,25", "vWA": "16,18", "THO1": "6,8", "TPOX": "8,11", "CSF1PO": "10,12", "D18S51": "13,19",
                   "D21S11": "30,32.2", "D2S441": "11,14", "D5S818": "12,12", "D7S82O": "8,10", "D12S391": "20,21",
                   "D13S317": "11,12", "D16S539": "12,14", "D19S433": "15.2,16", "D1S1656": "14,14", "D2S1338": "19,24",
                   "D3S1358": "16,16", "D6S1O43": "11,12", "D8S1179": "13,15", "Penta E": "7,11", "D1OS1248": "14,16",
                   "D22S1O45": "11,17"}
        )

        with open('upload_file/test_pdf/mother_and_child_22_name_on_rus.pdf', 'rb') as pdf_file:
            file_content = pdf_file.read()
            uploaded_file = InMemoryUploadedFile(file=ContentFile(file_content), field_name=None,
                                                 name='Даніель Фаріаш Гомес.pdf',
                                                 content_type='application/pdf', size=len(file_content),
                                                 content_type_extra=None, charset=None
                                                 )

        list_instance = [
            AwsMotherAndChildV3, AwsMotherAndChild, AwsMotherAndChildV2
        ]
        instance = self.mixin(uploaded_file, list_instance, 'media_jpg')
        father_dict = instance.process_file()
        response = instance.message_response(father_dict)
        instance.clean_folder()

        expected_response = {'log': 'caution', 'message': 'Даніель Фаріаш Гомес already exists'}
        self.assertEqual(response, expected_response)
        self.assertEqual(Client.objects.count(), 1)
