import logging
import os
import shutil
import fitz
import requests
import boto3
import botocore

from abc import ABC, abstractmethod
from decouple import config
from trp import Document

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

from upload_file.models import Client

LOCUS = {'D3S1358', 'vWA', 'D16S539', 'CSF1PO', 'TPOX', 'D8S1179', 'D21S11', 'D18S51', 'Penta E',
         'D2S441', 'D19S433', 'THO1', 'FGA', 'D22S1O45', 'D5S818', 'D13S317', 'D7S82O', 'D6S1O43',
         'D1OS1248', 'D1S1656', 'D12S391', 'D2S1338'}

logger = logging.getLogger(__name__)


class PlugToAWSMixin:
    def plug_to_aws(self):
        connected_aws = boto3.client(
            'textract', region_name='eu-west-2',
            aws_access_key_id=config("ACCESS_KEY_ID"),
            aws_secret_access_key=config('SECRET_ACCESS_KEY')
        )
        return connected_aws

    def analyze_document(self, binary, connected_aws, formatting=None):
        response = connected_aws.analyze_document(
            Document={'Bytes': binary},
            FeatureTypes=[formatting]
        )
        return response


class PdfExtractText(ABC):
    """
    Abstract class that specified method abstractmethod.
    All daughter classes which inheriting this base class
    must override 'extract_text_from_pdf' func
    """
    def __init__(self, client_instance: Client, image_folder: str) -> None:
        self.client_instance = client_instance
        self.image_folder = image_folder

    @abstractmethod
    def extract_text_from_pdf(self) -> dict: pass

    @staticmethod
    def process_string(input_str):
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


class PdfConvertIntoImageMixin:
    def pull_file(self, instance, output_folder):
        """Get file from remote storage"""
        response = requests.get(instance.get_file_url())
        local_file_path = f'{output_folder}/test.pdf'
        if response.status_code == 200:
            with open(local_file_path, 'wb') as f:
                f.write(response.content)
        return local_file_path

    def pdf_to_image(self, instance, index, output_folder, dpi=600):
        """Convert upload PDF file into image and save in 'media_jpg' dir"""
        local_file_path = self.pull_file(instance, output_folder)

        pdf_document = fitz.open(local_file_path)
        for i, page in enumerate(pdf_document):
            if i == index:
                image_path = f"{output_folder}/{instance.name}_{1}.jpg"
                image = page.get_pixmap(dpi=dpi)
                image.save(image_path)

                return image_path


class AwsEvrolab(PdfExtractText, PlugToAWSMixin):
    """
    Extract text from Evrolab pdf with aws microservice
    """

    def extract_text_from_pdf(self):
        """
        Getting father locus and his name from table
        """
        connected = self.plug_to_aws()
        file_binary = self.client_instance.file.read()
        response = self.analyze_document(file_binary, connected, formatting='TABLES')
        doc = Document(response)

        locus = {}

        for page in doc.pages:
            for table in page.tables:
                table_contains_locus = any(
                    len(row.cells) > 0 and
                    str(row.cells[0]).strip().replace('0', 'O').replace('I', '1') in LOCUS
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

        response = self.analyze_document(file_binary, connected, formatting='FORMS')
        name = self.name(response)

        return {'locus': locus, 'name': name}

    def name(self, response):
        doc = Document(response)
        name = next(
            (str(field.value).strip()
             for field in doc.pages[0].form.fields
             if str(field.key).strip() == 'Name:'),
            '')

        return name


class AwsEvrolabV2(PdfExtractText, PlugToAWSMixin, PdfConvertIntoImageMixin):
    """
    Extract text from Evrolab pdf page 1 with aws microservice
    """

    def analyze_document(self, image, connected_aws, formatting=None):

        with open(image, 'rb') as image_photo:
            binary = image_photo.read()

        return super().analyze_document(binary, connected_aws, formatting)

    def extract_text_from_pdf(self):
        """
        Getting father locus and his name from table
        """

        connected_aws = self.plug_to_aws()
        image = self.pdf_to_image(self.client_instance, 0, self.image_folder)
        response = self.analyze_document(image, connected_aws, formatting='TABLES')
        doc = Document(response)

        locus = {}
        name = ''

        page = doc.pages[0]
        if page.tables[2]:
            table = page.tables[2]

            for row in table.rows:
                first, second = row.cells[0:2]

                key = str(first).strip().replace('0', 'O').replace('I', '1')
                value = str(second).strip()

                if key in LOCUS and value:
                    value = self.process_string(value)
                    locus[key] = value

        if page.tables[1]:
            table = page.tables[1]

            for row in table.rows:
                first, second = row.cells[0:2]
                key = str(first).strip()
                if key == 'Name':
                    continue
                name += key
                if name:
                    break

        return {'locus': locus, 'name': name}

    def name(self, response):
        doc = Document(response)
        name = next(
            (str(field.value).strip()
             for field in doc.pages[0].form.fields
             if str(field.key).strip() == 'Name:'),
            '')

        return name


class AwsMotherAndChild(PdfExtractText, PlugToAWSMixin, PdfConvertIntoImageMixin):
    """
    Extract text from MotherAndChild pdf page 1 with aws microservice
    """

    def analyze_document(self, image, connected_aws, formatting=None):

        with open(image, 'rb') as image_photo:
            binary = image_photo.read()

        return super().analyze_document(binary, connected_aws, formatting)

    def extract_text_from_pdf(self):
        """
        Getting father locus and his name from table
        """
        connected_aws = self.plug_to_aws()
        image = self.pdf_to_image(self.client_instance, 0, self.image_folder)
        response = self.analyze_document(image, connected_aws, formatting='TABLES')
        doc = Document(response)

        locus = {}
        name = ''

        page = doc.pages[0]
        if page.tables[0]:
            table = page.tables[0]

            for row in table.rows:
                first, second = row.cells[0:2]

                key = str(first).strip().replace('0', 'O').replace('I', '1')
                value = str(second).strip()

                if key == 'Locus':
                    name += value
                if key in LOCUS and value:
                    value = self.process_string(value)
                    locus[key] = value

        return {'locus': locus, 'name': name}


class AwsMotherAndChildV2(PdfExtractText, PlugToAWSMixin, PdfConvertIntoImageMixin):
    """
    Extract text from MotherAndChild pdf page 3 with aws microservice
    """

    def analyze_document(self, image, connected_aws, formatting=None):

        with open(image, 'rb') as image_photo:
            binary = image_photo.read()

        return super().analyze_document(binary, connected_aws, formatting)

    def extract_text_from_pdf(self):
        """
        Getting father locus and his name from table
        """
        connected_aws = self.plug_to_aws()
        image = self.pdf_to_image(self.client_instance, 2, self.image_folder)
        response = self.analyze_document(image, connected_aws, formatting='TABLES')
        doc = Document(response)

        locus = {}
        name = ''

        page = doc.pages[0]
        if page.tables[0]:
            table = page.tables[0]

            for row in table.rows:
                first, second = row.cells[0:2]

                key = str(first).strip().replace('0', 'O').replace('I', '1')
                value = str(second).strip()

                if key == 'Locus':
                    name += value
                if key in LOCUS and value:
                    value = self.process_string(value)

                    locus[key] = value

        return {'locus': locus, 'name': name}


class AwsMotherAndChildV3(PdfExtractText, PlugToAWSMixin, PdfConvertIntoImageMixin):
    """
    Extract text from MotherAndChild pdf page 2 with aws microservice
    """

    def analyze_document(self, image, connected_aws, formatting=None):

        with open(image, 'rb') as image_photo:
            binary = image_photo.read()

        return super().analyze_document(binary, connected_aws, formatting)

    def extract_text_from_pdf(self):
        """
        Getting father locus and his name from table
        """
        connected_aws = self.plug_to_aws()
        image = self.pdf_to_image(self.client_instance, 1, self.image_folder)
        response = self.analyze_document(image, connected_aws, formatting='TABLES')
        doc = Document(response)

        locus = {}
        name = ''

        page = doc.pages[0]
        if page.tables[0]:
            table = page.tables[0]

            for row in table.rows:
                first, second = row.cells[0:2]

                key = str(first).strip().replace('0', 'O').replace('I', '1')
                value = str(second).strip()

                if key == 'Locus':
                    name += value
                if key in LOCUS and value:
                    value = self.process_string(value)
                    locus[key] = value

        return {'locus': locus, 'name': name}


class ProcessUploadedFile:

    def __init__(self, file: InMemoryUploadedFile, instance_list: list, folder: str) -> None:
        self.__file = file
        self.__instance_list = instance_list
        self.father = self.create_father(self.__file.name)
        self.path_folder = self.create_folder(folder)

    def create_folder(self, folder) -> str:
        path_to_folder = os.path.join(settings.BASE_DIR / folder)
        if not os.path.exists(path_to_folder):
            os.mkdir(path_to_folder)
        return path_to_folder

    def clean_folder(self) -> None:
        if os.path.exists(self.path_folder):
            shutil.rmtree(self.path_folder)

    def create_father(self, name: str) -> Client:
        father = Client.objects.create(name=name, file=self.__file)
        return father

    def process_file(self) -> dict:
        locus = ''
        name = ''
        for instance_class in iter(self.__instance_list):
            try:
                instance = instance_class(self.father, self.path_folder)
                father = instance.extract_text_from_pdf()
                locus, name = father.get('locus'), father.get('name')
                if locus:
                    if not name:
                        name = self.__file.name.strip('.pdf')
                    break
            except (Exception, botocore.exceptions.ClientError,
                    AttributeError, TypeError, IndexError) as e:
                logger.error(f'An error occurred: {str(e)}')
                continue

        if not locus and not name:
            self.father.delete()

        return {'locus': locus, 'name': name}

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
