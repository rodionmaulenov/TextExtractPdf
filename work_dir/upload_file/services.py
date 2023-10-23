import boto3
import botocore
import os
import fitz
import pdfplumber
import shutil
import logging

from abc import ABC, abstractmethod
from decouple import config
from io import BytesIO

import requests
from trp import Document

from django.conf import settings

from upload_file.models import Client

LOCUS = ['D3S1358', 'vWA', 'D16S539', 'CSF1PO', 'TPOX', 'D8S1179', 'D21S11', 'D18S51', 'Penta E',
         'D2S441', 'D19S433', 'THO1', 'FGA', 'D22S1O45', 'D5S818', 'D13S317', 'D7S82O', 'D6S1O43',
         'D1OS1248', 'D1S1656', 'D12S391', 'D2S1338']


class PdfExtractText(ABC):
    """
    Abstract class that specified method abstractmethod.
    All daughter classes which inheriting this base class
    must override 'extract_text_from_pdf' func
    """

    def __init__(self, pdf: BytesIO) -> None:
        self.file_pdf = pdf

    @abstractmethod
    def extract_text_from_pdf(self): pass


class PdfConvertIntoImage:
    def __init__(self, pdf: BytesIO) -> None:
        self.file_pdf = pdf

    def instance(self):
        instance = Client.objects.create(
            name=self.file_pdf.name,
            file_upload=self.file_pdf
        )
        return instance

    @property
    def path_save_image(self):
        path_save_image = os.path.join(settings.BASE_DIR / 'media_jpg')
        return path_save_image

    def get_image(self):
        instance = self.instance()
        if not os.path.exists(self.path_save_image):
            os.mkdir(self.path_save_image)

        image = self.pdf_to_image(instance, self.path_save_image)
        instance.delete()
        return image

    def pdf_to_image(self, instance, output_folder, dpi=300):
        """Convert upload PDF file into image and save in 'media_jpg' dir"""

        pdf_url = instance.get_file_url()
        response = requests.get(pdf_url)
        if response.status_code == 200:
            with open(f'{output_folder}/test.pdf', 'wb') as f:
                f.write(response.content)
        pdf_document = fitz.open(f'{output_folder}/test.pdf')
        for i, page in enumerate(pdf_document):
            if i == 0:
                image_path = f"{output_folder}/{instance.name}_{1}.jpg"
                image = page.get_pixmap(dpi=dpi)
                image.save(image_path)

                return image_path


class AwsEvrolab(PdfExtractText):
    """
    Extract text from Evrolab pdf with aws microservice
    """

    def plug_to_aws(self):

        connected_aws = boto3.client(
            'textract',
            region_name='eu-west-2',
            aws_access_key_id=config("ACCESS_KEY_ID"),
            aws_secret_access_key=config('SECRET_ACCESS_KEY')
        )

        return connected_aws

    def analyze_document(self, file_binary, connected_aws, formatting=None):

        response = connected_aws.analyze_document(
            Document={'Bytes': file_binary},
            FeatureTypes=[formatting]
        )
        doc = Document(response)

        return doc

    def extract_text_from_pdf(self):
        """
        Getting father locus and his name from table
        """
        connected = self.plug_to_aws()
        file_binary = self.file_pdf.read()
        doc = self.analyze_document(file_binary, connected, formatting='TABLES')

        locus = {}
        page = doc.pages[0]
        table = page.tables[2]
        for row in table.rows:
            first, second = row.cells[0:2]

            key = str(first).strip().replace('0', 'O')
            value = str(second).strip().replace(' ', '')

            if key in LOCUS:
                if value:
                    locus[key] = value

        doc = self.analyze_document(file_binary, connected, formatting='FORMS')
        name = self.get_name(doc)

        return {'locus': locus, 'name': name}

    def get_name(self, doc):
        name = ''
        for page in doc.pages:
            field = page.form.fields[14]

            key = str(field.key).strip()
            value = str(field.value).strip()

            if key == 'Name:':
                name += value
                break
        return name


class AwsMotherAndChild(PdfExtractText):
    """
    Extract text from MotherAndChild pdf with aws microservice
    """

    def plug_to_aws(self):
        connected_aws = boto3.client(
            'textract', region_name='eu-west-2',
            aws_access_key_id=config("ACCESS_KEY_ID"),
            aws_secret_access_key=config('SECRET_ACCESS_KEY')
        )
        return connected_aws

    def analyze_document(self, connected_aws, formatting=None):

        image = self.transformer.get_image()

        with open(image, 'rb') as image_photo:
            file_binary = image_photo.read()

        response = connected_aws.analyze_document(
            Document={'Bytes': file_binary},
            FeatureTypes=[formatting]
        )
        doc = Document(response)

        self.remove_path()

        return doc

    def extract_text_from_pdf(self):
        """
        Getting father locus and his name from table
        """
        connected_aws = self.plug_to_aws()
        doc = self.analyze_document(connected_aws, formatting='TABLES')

        locus = {}
        name = ''
        page = doc.pages[0]
        table = page.tables[0]
        for row in table.rows:
            first, second = row.cells[0:2]

            key = str(first).strip().replace('0', 'O')
            value = str(second).strip()

            if key == 'Locus':
                name += value
            if key in LOCUS:
                locus = locus
                if value:
                    value = value.replace(' ', '')
                    locus[key] = value

        return {'locus': locus, 'name': name}

    @property
    def transformer(self):
        pdf_to_image = PdfConvertIntoImage(self.file_pdf)
        return pdf_to_image

    def remove_path(self):
        if os.path.exists(self.transformer.path_save_image):
            shutil.rmtree(self.transformer.path_save_image)


class PdfPlumberMotherAndChild(PdfExtractText):
    """
    Extract text from MotherAndChild pdf where
    not requiring to use aws service
    """

    def get_table_page(self):
        """Get specified page from PDF file"""
        with pdfplumber.open(self.file_pdf) as pdf:
            page = pdf.pages[2]

        return page

    def extract_text_from_pdf(self):
        """
        Getting father locus and his name from table
        """
        page = self.get_table_page()
        table = page.extract_table()

        name = ''
        locus = {}
        if 'Locus' in table[0]:
            name += table[0][1]
            for row in table:
                key, value = row

                key = key.replace('0', 'O')
                value = value.replace(' ', '')

                if key in LOCUS:
                    if value:
                        locus[key] = value

        return {'locus': locus, 'name': name}


logger = logging.getLogger(__name__)


class ProcessUploadedFile:
    """
    In for loop using instances that extract text from the PDF
    in different ways and at the end return a final
    response message about the status of the PDF extraction.
    """

    def __init__(self, pdf: BytesIO, instances_list: list) -> None:
        self.file_pdf = pdf
        self.instances_extract_text = instances_list

    def process_uploaded_file(self) -> dict:
        father = {}
        for instance in self.instances_extract_text:
            try:
                instance = instance(self.file_pdf)
                father = instance.extract_text_from_pdf()
            except botocore.exceptions.ClientError:
                continue
            except (AttributeError, TypeError, IndexError):
                continue
            except Exception as e:
                logger.error(f'An error occurred: {str(e)}')
                continue

            if father.get('locus') and father.get('name'):
                break
            else:
                continue

        if father.get('locus') and not father.get('name'):
            name = self.file_pdf.name.strip('.pdf')
            father['name'] = name

        return father

    def get_message_response(self):
        father = self.process_uploaded_file()

        if father.get('locus') and father.get('name'):
            name = father['name']
            locus = father['locus']

            instance, created = Client.objects.get_or_create(
                name=name,
                locus=locus
            )

            if created:
                instance.name = name
                instance.locus = locus
                instance.file_upload = self.file_pdf
                instance.save()
                return {'message': f'Father {name} saved successfully', 'log': 'success'}
            else:
                return {'message': f'Father {name} already exists', 'log': 'caution'}
        else:
            message = {'message': 'Error processing', 'log': 'error'}
            return message
