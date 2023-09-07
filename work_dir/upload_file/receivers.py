import os


def delete_client_pdf_file(sender, **kwargs):
    client = kwargs.get('instance')
    pdf_file_path = client.file_upload.path
    print(pdf_file_path)
    if os.path.exists(pdf_file_path):
        os.remove(pdf_file_path)
