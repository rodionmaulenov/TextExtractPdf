import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from upload_file.models import Client


class ClientFileDeleteTest(TestCase):

    def setUp(self):
        # Create a test Client instance with a PDF file
        pdf_file_content = b"PDF file content"
        self.client_instance = Client.objects.create(
            name="Test Client",
            file_upload=SimpleUploadedFile("test.pdf", pdf_file_content),
        )

    def test_delete_client_deletes_pdf_file(self):
        # Get the path to the PDF file before deleting the client
        pdf_file_path = self.client_instance.file_upload.path

        # Delete the client instance
        self.client_instance.delete()

        # Check if the PDF file still exists on the file system
        self.assertFalse(os.path.exists(pdf_file_path), f"PDF file {pdf_file_path} should be deleted")

    def tearDown(self):
        # Clean up any files created during testing
        self.client_instance.file_upload.delete()
