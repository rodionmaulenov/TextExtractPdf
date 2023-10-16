# import boto3
# import botocore
# import os
# import fitz
# import pdfplumber
# import shutil
# from decouple import config
# from trp import Document
#
# from django.conf import settings
#
# from upload_file.models import Client
#
# LOCUS = ['D3S1358', 'vWA', 'D16S539', 'CSF1PO', 'TPOX', 'D8S1179', 'D21S11', 'D18S51', 'Penta E',
#          'D2S441', 'D19S433', 'THO1', 'FGA', 'D22S1O45', 'D5S818', 'D13S317', 'D7S82O', 'D6S1O43',
#          'D1OS1248', 'D1S1656', 'D12S391', 'D2S1338']
#
#
# class AWSPdfTextExtractMixin:
#     def get_locus_and_name_from_evrolab(self, textract, file_binary):
#         response = textract.analyze_document(
#             Document={'Bytes': file_binary},
#             FeatureTypes=['TABLES']
#         )
#         doc = Document(response)
#
#         father_locus = {}
#         locus_key = None
#         for p, page in enumerate(doc.pages):
#             if p == 0:
#                 for t, table in enumerate(page.tables):
#                     if t == 2:
#                         for row in table.rows:
#                             for c, cell in enumerate(row.cells):
#                                 if c <= 1:
#                                     changing = str(cell).strip().replace('0', 'O')
#                                     if changing in LOCUS:
#                                         locus_key = changing
#                                         continue
#                                     if locus_key and c == 1:
#                                         locus_value = str(cell).replace(' ', '')
#                                         if locus_value:
#                                             father_locus[locus_key] = locus_value
#                                         locus_key = None
#                                         if len(father_locus) == 15:
#                                             locus_key = None
#                                             break
#
#         response = textract.analyze_document(
#             Document={'Bytes': file_binary},
#             FeatureTypes=['FORMS']
#         )
#         doc = Document(response)
#
#         father_name = None
#         for page in doc.pages:
#             for field in page.form.fields:
#                 if str(field.key).strip() == 'Name:':
#                     father_name = str(field.value).strip()
#                     break
#
#         return father_locus, father_name
#
#     def get_aws_father_locus_and_name(self, file_pdf):
#         """Get specified page from PDF file"""
#
#         textract = boto3.client(
#             'textract', region_name='eu-west-2',
#             aws_access_key_id=config("ACCESS_KEY_ID"),
#             aws_secret_access_key=config('SECRET_ACCESS_KEY')
#         )
#
#         try:
#             file_binary = file_pdf.read()
#             father_locus, father_name = self.get_locus_and_name_from_evrolab(textract, file_binary)
#             return father_locus, father_name
#
#         except AttributeError:
#             with open(file_pdf, 'rb') as image_photo:
#                 file_binary = image_photo.read()
#
#             response = textract.analyze_document(
#                 Document={'Bytes': file_binary},
#                 FeatureTypes=['TABLES']
#             )
#             doc = Document(response)
#
#             father_locus = {}
#             name = None
#             name_key = None
#             locus_key = None
#             for p, page in enumerate(doc.pages):
#                 if p == 0:
#                     for t, table in enumerate(page.tables):
#                         if t == 0:
#                             for row in table.rows:
#                                 for c, cell in enumerate(row.cells):
#                                     if c <= 1:
#                                         locus = str(cell).strip().replace('0', 'O')
#                                         if str(cell).strip() == 'Locus':
#                                             name_key = 'name'
#                                         if name_key and c == 1:
#                                             name = str(cell).strip()
#                                             name_key = None
#                                         if locus in LOCUS:
#                                             locus_key = locus
#                                             continue
#                                         if locus_key and c == 1:
#                                             locus_value = str(cell).replace(' ', '')
#                                             if locus_value:
#                                                 father_locus[locus_key] = locus_value
#                                             locus_key = None
#             return father_locus, name
#
#
# class PdfTextExtractMixin(AWSPdfTextExtractMixin):
#
#     def convert_pdf_to_images(sekf, pdf_file, output_folder, dpi=300):
#         """Convert upload PDF file into image and save in 'media_jpg' dir"""
#
#         pdf_document = fitz.open(pdf_file.path)
#         for i, page in enumerate(pdf_document):
#             if i == 0:
#                 image_path = f"{output_folder}/{pdf_file.name}_{1}.jpg"
#                 image = page.get_pixmap(dpi=dpi)
#                 image.save(image_path)
#
#                 return image_path
#
#     def get_table_page(self, file_pdf, page):
#         """Get specified page from PDF file"""
#
#         with pdfplumber.open(file_pdf) as pdf:
#             try:
#                 page = pdf.pages[page]
#                 return page
#
#             except IndexError:
#                 return None
#
#     def get_locus_and_name_from_image(self, file_pdf):
#         """
#         Get locus and name from convert PDF file into Image
#         if PDF file not read from pdfplumber.open()
#         """
#
#         client = Client.objects.create(
#             name=file_pdf.name,
#             file_upload=file_pdf
#         )
#
#         full_path = client.file_upload
#         path_save_image = os.path.join(settings.BASE_DIR / 'media_jpg')
#         os.mkdir(path_save_image)
#         image = self.convert_pdf_to_images(full_path, path_save_image)
#         father_locus, father_name = self.get_aws_father_locus_and_name(image)
#         if father_locus and not father_name:
#             father_name = file_pdf.name.strip(".pdf")
#         shutil.rmtree(path_save_image)
#         client.delete()
#
#         return father_locus, father_name
#
#     def get_father_locus_and_name(self, file_pdf):
#         """
#         Getting father locus and his name from table
#         in other case return None
#         """
#         try:
#             for num in range(3):
#                 page = self.get_table_page(file_pdf, num)
#                 table = page.extract_table()
#
#                 if table is None and num == 0:
#                     father_locus, father_name = self.get_locus_and_name_from_image(file_pdf)
#                     return father_locus, father_name
#
#                 if 'Locus' in table[0] and num == 2:
#                     father_locus = {}
#                     for row in table:
#                         key = row[0].replace('0', 'O') if row[0] is not None and '0' in row[0] else row[0]
#                         if key in LOCUS:
#                             if row[1]:
#                                 father_locus[key] = row[1].replace(' ', '')
#
#                     all_pdf = page.extract_text()
#                     lines = all_pdf.split('\n')
#
#                     father_name = ''
#                     if 'Patient DNA test results' in all_pdf:
#                         for line in lines:
#                             if 'Locus' in line:
#                                 father_name += (line.split()[1] + ' ' + line.split()[2]).strip()
#                             if father_name:
#                                 break
#
#                         if father_locus and father_name:
#                             return father_locus, father_name
#
#         except Exception:
#             return None, None
#
#         return None, None
#
#
# class ProcessUploadedFileMixin(PdfTextExtractMixin):
#     def process_uploaded_file(self, uploaded_file):
#         """
#         Main logic how to upload, validating logic, getting table page, and save
#         pdf file
#         """
#
#         try:
#             locus, name = self.get_aws_father_locus_and_name(uploaded_file)
#         except botocore.exceptions.ClientError:
#             locus, name = self.get_father_locus_and_name(uploaded_file)
#
#         father_dict = self.get_message(locus, name)
#
#         if "father_name" in father_dict and 'father_locus' in father_dict:
#             father_name = father_dict.get('father_name')
#             father_locus = father_dict.get('father_locus')
#
#             father, created = Client.objects.get_or_create(
#                 name=father_name,
#                 locus=father_locus
#             )
#
#             if created:
#                 father.name = father_name
#                 father.locus = father_locus
#                 father.file_upload = uploaded_file
#                 father.save()
#                 return {'message': f'Father {father_name} saved successfully', 'log': 'success'}
#             else:
#                 return {'message': f'Father {father_name} already exists', 'log': 'caution'}
#         else:
#             message = father_dict
#             return message
#
#     def get_message(self, locus, name):
#         father_or_message = {}
#         if locus and name:
#             father_or_message['father_locus'] = locus
#             father_or_message['father_name'] = name
#             return father_or_message
#         else:
#             father_or_message['message'] = 'Error processing'
#             father_or_message['log'] = 'error'
#             return father_or_message


import boto3
import botocore
from abc import ABC, abstractmethod
import os
import fitz
import pdfplumber
import shutil
from decouple import config
from trp import Document

from django.conf import settings

from upload_file.models import Client

LOCUS = ['D3S1358', 'vWA', 'D16S539', 'CSF1PO', 'TPOX', 'D8S1179', 'D21S11', 'D18S51', 'Penta E',
         'D2S441', 'D19S433', 'THO1', 'FGA', 'D22S1O45', 'D5S818', 'D13S317', 'D7S82O', 'D6S1O43',
         'D1OS1248', 'D1S1656', 'D12S391', 'D2S1338']


class PdfExtractText(ABC):
    @abstractmethod
    def extract_text_from_pdf(self): pass


class PdfConvertIntoImage:
    def __init__(self, pdf):
        self.file_pdf = pdf

    def get_image(self):

        client = Client.objects.create(
            name=self.file_pdf.name,
            file_upload=self.file_pdf
        )

        file_upload = client.file_upload
        path_save_image = os.path.join(settings.BASE_DIR / 'media_jpg')
        os.mkdir(path_save_image)
        pdf_converter = PdfConvertIntoImage(self.file_pdf)
        image = pdf_converter.convert_pdf_to_image(file_upload, path_save_image)
        return image, client, path_save_image

    def convert_pdf_to_image(self, file_upload, output_folder, dpi=300):
        """Convert upload PDF file into image and save in 'media_jpg' dir"""

        pdf_document = fitz.open(file_upload.path)
        for i, page in enumerate(pdf_document):
            if i == 0:
                image_path = f"{output_folder}/{file_upload.name}_{1}.jpg"
                image = page.get_pixmap(dpi=dpi)
                image.save(image_path)

                return image_path


class AwsEvrolab(PdfExtractText):

    def __init__(self, pdf):
        self.file_pdf = pdf

    def connect_aws_service(self):

        connected_aws = boto3.client(
            'textract', region_name='eu-west-2',
            aws_access_key_id=config("ACCESS_KEY_ID"),
            aws_secret_access_key=config('SECRET_ACCESS_KEY')
        )

        file_binary = self.file_pdf.read()

        return connected_aws, file_binary

    def analyze_document(self, file_binary, connected_aws, formatting=None):

        response = connected_aws.analyze_document(
            Document={'Bytes': file_binary},
            FeatureTypes=[formatting]
        )
        doc = Document(response)

        return doc

    def extract_text_from_pdf(self):

        connected, file_binary = self.connect_aws_service()
        doc = self.analyze_document(file_binary, connected, formatting='TABLES')

        father_locus = {}
        locus_key = None
        for p, page in enumerate(doc.pages):
            if p == 0:
                for t, table in enumerate(page.tables):
                    if t == 2:
                        for row in table.rows:
                            for c, cell in enumerate(row.cells):
                                if c <= 1:
                                    changing = str(cell).strip().replace('0', 'O')
                                    if changing in LOCUS:
                                        locus_key = changing
                                        continue
                                    if locus_key and c == 1:
                                        locus_value = str(cell).replace(' ', '')
                                        if locus_value:
                                            father_locus[locus_key] = locus_value
                                        locus_key = None
                                        if len(father_locus) == 15:
                                            locus_key = None
                                            break

        doc = self.analyze_document(file_binary, connected, formatting='FORMS')
        father_name = self.get_name(doc)

        return father_locus, father_name

    def get_name(self, doc):
        father_name = None
        for page in doc.pages:
            for field in page.form.fields:
                if str(field.key).strip() == 'Name:':
                    father_name = str(field.value).strip()
                    break
        return father_name


class AwsMotherAndChild(PdfExtractText):

    def __init__(self, pdf):
        self.file_pdf = pdf

    def connect_aws_service(self):
        connected_aws = boto3.client(
            'textract', region_name='eu-west-2',
            aws_access_key_id=config("ACCESS_KEY_ID"),
            aws_secret_access_key=config('SECRET_ACCESS_KEY')
        )
        return connected_aws

    def analyze_document(self, connected_aws, formatting=None):

        image = PdfConvertIntoImage(self.file_pdf)
        image, client, path_save_image = image.get_image()

        with open(image, 'rb') as image_photo:
            file_binary = image_photo.read()

        response = connected_aws.analyze_document(
            Document={'Bytes': file_binary},
            FeatureTypes=[formatting]
        )
        doc = Document(response)

        shutil.rmtree(path_save_image)
        client.delete()

        return doc

    def extract_text_from_pdf(self):
        """Get specified page from PDF file"""

        connected_aws = self.connect_aws_service()
        doc = self.analyze_document(connected_aws, formatting='TABLES')

        father_locus = {}
        name = None
        name_key = None
        locus_key = None
        for p, page in enumerate(doc.pages):
            if p == 0:
                for t, table in enumerate(page.tables):
                    if t == 0:
                        for row in table.rows:
                            for c, cell in enumerate(row.cells):
                                if c <= 1:
                                    locus = str(cell).strip().replace('0', 'O')
                                    if str(cell).strip() == 'Locus':
                                        name_key = 'name'
                                    if name_key and c == 1:
                                        name = str(cell).strip()
                                        name_key = None
                                    if locus in LOCUS:
                                        locus_key = locus
                                        continue
                                    if locus_key and c == 1:
                                        locus_value = str(cell).replace(' ', '')
                                        if locus_value:
                                            father_locus[locus_key] = locus_value
                                        locus_key = None

        return father_locus, name


class PdfPlumberMotherAndChild(PdfExtractText):

    def __init__(self, pdf):
        self.file_pdf = pdf

    def get_table_page(self):
        """Get specified page from PDF file"""

        with pdfplumber.open(self.file_pdf) as pdf:
            page = pdf.pages[2]

        return page

    def extract_text_from_pdf(self):
        """
        Getting father locus and his name from table
        in other case return None
        """
        page = self.get_table_page()
        table = page.extract_table()

        if 'Locus' in table[0]:
            father_locus = {}
            for row in table:
                key = row[0].replace('0', 'O') if row[0] is not None and '0' in row[0] else row[0]
                if key in LOCUS:
                    if row[1]:
                        father_locus[key] = row[1].replace(' ', '')

            all_pdf = page.extract_text()
            lines = all_pdf.split('\n')

            father_name = ''
            if 'Patient DNA test results' in all_pdf:
                for line in lines:
                    if 'Locus' in line:
                        father_name += (line.split()[1] + ' ' + line.split()[2]).strip()
                    if father_name:
                        break

                if father_locus and father_name:
                    return father_locus, father_name

        return None, None


class ProcessUploadedFile:
    def __init__(self, pdf, instance: list):
        self.file_pdf = pdf
        self.instances_get_text_from_pdf = instance

    def process_uploaded_file(self, uploaded_file):
        """
        Main logic how to upload, validating logic, getting tablel page, and save
        pdf file
        """
        locus = None
        name = None
        for instance in self.instances_get_text_from_pdf:
            try:
                instance = instance(self.file_pdf)
                locus, name = instance.extract_text_from_pdf()
            except botocore.exceptions.ClientError as e:
                continue
            except (AttributeError, TypeError, IndexError):
                continue

            if locus is None and name is None:
                continue
            else:
                break

        if locus and name is None:
            name = self.file_pdf.name.strip('.pdf')

        father_dict = self.get_message(locus, name)

        if "father_name" in father_dict and 'father_locus' in father_dict:
            father_name = father_dict.get('father_name')
            father_locus = father_dict.get('father_locus')

            father, created = Client.objects.get_or_create(
                name=father_name,
                locus=father_locus
            )

            if created:
                father.name = father_name
                father.locus = father_locus
                father.file_upload = uploaded_file
                father.save()
                return {'message': f'Father {father_name} saved successfully', 'log': 'success'}
            else:
                return {'message': f'Father {father_name} already exists', 'log': 'caution'}
        else:
            message = father_dict
            return message

    def get_message(self, locus, name):
        father_or_message = {}
        if locus and name:
            father_or_message['father_locus'] = locus
            father_or_message['father_name'] = name
            return father_or_message
        else:
            father_or_message['message'] = 'Error processing'
            father_or_message['log'] = 'error'
            return father_or_message
