import os


def delete_client_pdf_file(sender, instance, **kwargs):
    if hasattr(instance, 'file_upload') and instance.file_upload:
        pdf_file_path = instance.file_upload.path
        if os.path.exists(pdf_file_path):
            os.remove(pdf_file_path)
