from django.conf import settings
from django.db import models


def user_directory_path(instance, filename):
    return instance.name


class Client(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True, unique=True)
    locus = models.JSONField(blank=True, null=True)
    file_upload = models.FileField(upload_to=user_directory_path)
    date_create = models.DateField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_file_url(self):
        if self.file_upload:
            return settings.MEDIA_URL + str(self.file_upload)
        return None
