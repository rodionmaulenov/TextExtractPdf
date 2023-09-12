from django.db import models
from django.db.models.signals import pre_delete

from upload_file.receivers import delete_client_pdf_file


def user_directory_path(instance, filename):
    return f"{'*'.join(instance.name.split())}.pdf"


# storage=MediaRootS3BotoStorage() if 'prod' in os.environ.get('DJANGO_SETTINGS_MODULE') else FileSystemStorage()

class Client(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    locus = models.JSONField(blank=True, null=True)
    file_upload = models.FileField(upload_to=user_directory_path)
    date_create = models.DateField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


pre_delete.connect(delete_client_pdf_file, sender=Client)


class Child(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name


class DNK(models.Model):
    child = models.OneToOneField(Child, on_delete=models.PROTECT, null=True, blank=True)

    D3S1358 = models.CharField(max_length=10, null=True, blank=True)
    vWA = models.CharField(max_length=10, null=True, blank=True)
    D16S539 = models.CharField(max_length=10, null=True, blank=True)
    CSF1P0 = models.CharField(max_length=10, null=True, blank=True)
    TPOX = models.CharField(max_length=10, null=True, blank=True)
    D8S1179 = models.CharField(max_length=10, null=True, blank=True)
    D21S11 = models.CharField(max_length=10, null=True, blank=True)
    D18S51 = models.CharField(max_length=10, null=True, blank=True)
    Penta_E = models.CharField(max_length=10, verbose_name='Penta E', null=True, blank=True)
    D2S441 = models.CharField(max_length=10, null=True, blank=True)
    D19S433 = models.CharField(max_length=10, null=True, blank=True)
    THO1 = models.CharField(max_length=10, null=True, blank=True)
    FGA = models.CharField(max_length=10, null=True, blank=True)
    D22S1045 = models.CharField(max_length=10, null=True, blank=True)
    D5S818 = models.CharField(max_length=10, null=True, blank=True)
    D13S317 = models.CharField(max_length=10, null=True, blank=True)
    D7S820 = models.CharField(max_length=10, null=True, blank=True)
    D6S1043 = models.CharField(max_length=10, null=True, blank=True)
    D10S1248 = models.CharField(max_length=10, null=True, blank=True, )
    D1S1656 = models.CharField(max_length=10, null=True, blank=True)
    D12S391 = models.CharField(max_length=10, null=True, blank=True)
    D2S1338 = models.CharField(max_length=10, null=True, blank=True)
    Penta_D = models.CharField(max_length=10, verbose_name='Penta D', null=True, blank=True)
