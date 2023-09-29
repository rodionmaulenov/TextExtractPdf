from django.db import models
from django.db.models.signals import pre_delete

from upload_file.receivers import delete_client_pdf_file


def user_directory_path(instance, filename):
    return f"{instance.name}.pdf"


class Client(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    locus = models.JSONField(blank=True, null=True)
    file_upload = models.FileField(upload_to=user_directory_path)
    date_create = models.DateField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


pre_delete.connect(delete_client_pdf_file, sender=Client)

