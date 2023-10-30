import os
import shutil
import fitz
import requests
import boto3
import botocore

from abc import ABC, abstractmethod
from decouple import config
from trp import Document
from typing import Type

from django.db import transaction
from django.db import models
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

from upload_file.models import Client

LOCUS = {'D3S1358', 'vWA', 'D16S539', 'CSF1PO', 'TPOX', 'D8S1179', 'D21S11', 'D18S51', 'Penta E',
         'D2S441', 'D19S433', 'THO1', 'FGA', 'D22S1O45', 'D5S818', 'D13S317', 'D7S82O', 'D6S1O43',
         'D1OS1248', 'D1S1656', 'D12S391', 'D2S1338'}


class PdfExtractText(ABC):
    """
    Abstract class that specified method abstractmethod.
    All daughter classes which inheriting this base class
    must override 'extract_text_from_pdf' func
    """

    def __init__(self, instance_id: int) -> None:
        self.instance_id = instance_id

    @abstractmethod
    def extract_text_from_pdf(self) -> dict:
        pass

    def process_string(self, input_str):
        input_str = input_str.replace(' ', '')

        comma_count = input_str.count(',')
        dot_count = input_str.count('.')

        if comma_count == 1:
            return input_str
        elif dot_count == 1 and comma_count == 0:
            return input_str.replace('.', ',')
        elif dot_count == 2:
            parts = input_str.split('.')
            variant1 = parts[0] + ',' + parts[1] + '.' + '.'.join(parts[2:])
            variant2 = parts[0] + '.' + parts[1] + ',' + parts[2]
            return f"{variant1},{variant2}"
        elif dot_count == 3:
            second_dot_index = input_str.find('.', input_str.find('.') + 1)
            return input_str[:second_dot_index] + ',' + input_str[second_dot_index + 1:]
        return input_str


class PdfConvertIntoImage:
    def __init__(self, instance: Client, page: int) -> None:
        self.instance = instance
        self.page = page

    @property
    def path_save_image(self):
        path_save_image = os.path.join(settings.BASE_DIR / 'media_jpg')
        return path_save_image

    def get_image(self):
        if not os.path.exists(self.path_save_image):
            os.mkdir(self.path_save_image)

        image = self.pdf_to_image(self.path_save_image)
        return image

    def pdf_to_image(self, output_folder, dpi=300):
        """Convert upload PDF file into image and save in 'media_jpg' dir"""

        response = requests.get(self.instance.get_file_url())
        if response.status_code == 200:
            with open(f'{output_folder}/test.pdf', 'wb') as f:
                f.write(response.content)
        pdf_document = fitz.open(f'{output_folder}/test.pdf')
        for i, page in enumerate(pdf_document):
            if i == self.page:
                image_path = f"{output_folder}/{self.instance.name}_{1}.jpg"
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

    def instance(self, Model: models):
        father = Model.objects.get(id=self.instance_id)
        file_binary = father.file.read()

        return file_binary

    def extract_text_from_pdf(self):
        """
        Getting father locus and his name from table
        """

        connected = self.plug_to_aws()
        file_binary = self.instance(Client)
        doc = self.analyze_document(file_binary, connected, formatting='TABLES')

        locus = {}

        for page in doc.pages:
            for table in page.tables:
                table_contains_locus = any(
                    len(row.cells) > 0 and
                    str(row.cells[0]).strip().replace('0', 'O') in LOCUS
                    for row in table.rows
                )

                if table_contains_locus:
                    locus = {
                        str(cell[0]).strip().replace('0', 'O'):
                            self.process_string(str(cell[1]))
                        for row in table.rows
                        if len(row.cells) >= 2
                        for cell in [row.cells[0:2]]
                        if str(cell[0]).strip().replace('0', 'O') in LOCUS and cell[1]
                    }
                    break

        doc = self.analyze_document(file_binary, connected, formatting='FORMS')
        name = self.name(doc)

        return {'locus': locus, 'name': name}

    def name(self, doc):
        name = next(
            (str(field.value).strip()
             for field in doc.pages[0].form.fields
             if str(field.key).strip() == 'Name:'),
            '')

        return name


class AwsMotherAndChild(PdfExtractText):
    """
    Extract text from MotherAndChild pdf page 1 with aws microservice
    """

    def plug_to_aws(self):
        connected_aws = boto3.client(
            'textract', region_name='eu-west-2',
            aws_access_key_id=config("ACCESS_KEY_ID"),
            aws_secret_access_key=config('SECRET_ACCESS_KEY')
        )
        return connected_aws

    def analyze_document(self, image, connected_aws, formatting=None):

        with open(image, 'rb') as image_photo:
            binary = image_photo.read()

        response = connected_aws.analyze_document(
            Document={'Bytes': binary},
            FeatureTypes=[formatting]
        )
        doc = Document(response)

        return doc

    def father_instance(self, Model: models):
        with transaction.atomic():
            instance = Model.objects.select_for_update().get(id=self.instance_id)
        return instance

    def extract_text_from_pdf(self):
        """
        Getting father locus and his name from table
        """
        connected_aws = self.plug_to_aws()
        instance = self.father_instance(Client)
        image = PdfConvertIntoImage(instance, 0).get_image()
        doc = self.analyze_document(image, connected_aws, formatting='TABLES')

        locus = {}
        name = ''

        page = doc.pages[0]
        if page.tables[0]:
            table = page.tables[0]

            for row in table.rows:
                first, second = row.cells[0:2]

                key = str(first).strip().replace('0', 'O')
                value = str(second).strip()

                if key == 'Locus':
                    name += value
                if key in LOCUS and value:
                    value = self.process_string(value)
                    locus[key] = value

        return {'locus': locus, 'name': name}


class AwsMotherAndChildV2(PdfExtractText):
    """
    Extract text from MotherAndChild pdf page 3 with aws microservice
    """

    def plug_to_aws(self):
        connected_aws = boto3.client(
            'textract', region_name='eu-west-2',
            aws_access_key_id=config("ACCESS_KEY_ID"),
            aws_secret_access_key=config('SECRET_ACCESS_KEY')
        )
        return connected_aws

    def analyze_document(self, image, connected_aws, formatting=None):

        with open(image, 'rb') as image_photo:
            binary = image_photo.read()

        response = connected_aws.analyze_document(
            Document={'Bytes': binary},
            FeatureTypes=[formatting]
        )
        doc = Document(response)

        return doc

    def father_instance(self, Model: models):
        with transaction.atomic():
            instance = Model.objects.select_for_update().get(id=self.instance_id)
        return instance

    def extract_text_from_pdf(self):
        """
        Getting father locus and his name from table
        """
        connected_aws = self.plug_to_aws()
        instance = self.father_instance(Client)
        image = PdfConvertIntoImage(instance, 2).get_image()
        doc = self.analyze_document(image, connected_aws, formatting='TABLES')

        locus = {}
        name = ''

        page = doc.pages[0]
        if page.tables[0]:
            table = page.tables[0]

            for row in table.rows:
                first, second = row.cells[0:2]

                key = str(first).strip().replace('0', 'O')
                value = str(second).strip()

                if key == 'Locus':
                    name += value
                if key in LOCUS and value:
                    value = self.process_string(value)

                    locus[key] = value

        return {'locus': locus, 'name': name}


class AwsMotherAndChildV3(PdfExtractText):
    """
    Extract text from MotherAndChild pdf page 3 with aws microservice
    """

    def plug_to_aws(self):
        connected_aws = boto3.client(
            'textract', region_name='eu-west-2',
            aws_access_key_id=config("ACCESS_KEY_ID"),
            aws_secret_access_key=config('SECRET_ACCESS_KEY')
        )
        return connected_aws

    def analyze_document(self, image, connected_aws, formatting=None):

        with open(image, 'rb') as image_photo:
            binary = image_photo.read()

        response = connected_aws.analyze_document(
            Document={'Bytes': binary},
            FeatureTypes=[formatting]
        )
        doc = Document(response)

        return doc

    def father_instance(self, Model: models):
        with transaction.atomic():
            instance = Model.objects.select_for_update().get(id=self.instance_id)
        return instance

    def extract_text_from_pdf(self):
        """
        Getting father locus and his name from table
        """
        connected_aws = self.plug_to_aws()
        instance = self.father_instance(Client)
        image = PdfConvertIntoImage(instance, 1).get_image()
        doc = self.analyze_document(image, connected_aws, formatting='TABLES')

        locus = {}
        name = ''

        page = doc.pages[0]
        if page.tables[0]:
            table = page.tables[0]

            for row in table.rows:
                first, second = row.cells[0:2]

                key = str(first).strip().replace('0', 'O')
                value = str(second).strip()

                if key == 'Locus':
                    name += value
                if key in LOCUS and value:
                    value = self.process_string(value)
                    locus[key] = value

        return {'locus': locus, 'name': name}


class FatherInstance:

    def __set_name__(self, owner: Type, name: str):
        self.father = '_' + name

    def __get__(self, obj: Client, objtype=None) -> Client:
        return getattr(obj, self.father)


class ProcessUploadedFile:
    father = FatherInstance()

    def __init__(self, file: InMemoryUploadedFile, instance_list: list) -> None:
        self.__file = file
        self.__instance_list = instance_list
        self.father = self.create_father(self.__file.name)

    def create_father(self, name: str) -> Client:
        father = Client.objects.create(name=name, file=self.__file)
        return father

    def process_uploaded_file(self) -> dict:
        locus = ''
        name = ''
        for instance_class in iter(self.__instance_list):
            try:
                instance = instance_class(self.father.id)
                father = instance.extract_text_from_pdf()
                locus, name = father.get('locus'), father.get('name')
                if locus:
                    if not name:
                        name = self.__file.name.strip('.pdf')
                    break
            except (Exception, botocore.exceptions.ClientError, AttributeError, TypeError, IndexError) as e:
                continue

        if not locus and not name:
            self.father.delete()

        return {'locus': locus, 'name': name}

    def clean_up_files(self) -> None:
        path_save_image = os.path.join(settings.BASE_DIR, 'media_jpg')
        if os.path.exists(path_save_image):
            shutil.rmtree(path_save_image)

    def message_response(self, father: dict) -> dict:
        locus, name = father['locus'], father['name']
        if locus and name:
            try:
                Client.objects.get(name=name, locus=locus)
                self.father.delete()
                return {'message': f'{name} already exists', 'log': 'caution'}
            except Client.DoesNotExist:
                self.father.name = name
                self.father.locus = locus
                self.father.save()
                return {'message': f'{name} saved successfully', 'log': 'success'}
        else:
            return {'message': 'Error processing file', 'log': 'error'}
