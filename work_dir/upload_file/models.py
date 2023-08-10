from django.db import models


def user_directory_path(instance, filename):
    return f"{'*'.join(instance.name.split())}.pdf"


class Client(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    locus = models.JSONField(blank=True, null=True)
    file_upload = models.FileField(upload_to=user_directory_path)
    date_create = models.DateField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Child(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True)

    # def __str__(self):
    #     return self.name


class DNK(models.Model):
    LOCUS = [
        ('D3S1358', 'D3S1358'), ('vWa', 'vWa'), ('D16S539', 'D16S539'),
        ('CSF1P0', 'CSF1P0'), ('TPOX', 'TPOX'), ('D8S1179', 'D8S1179'),
        ('D21S11', 'D21S11'), ('D18S51', 'D18S51'), ('Penta E', 'Penta E'),
        ('D2S441', 'D2S441'), ('D19S433', 'D19S433'), ('THO1 E', 'THO1 E'),
        ('FGA', 'FGA'), ('D22S1045', 'D22S1045'), ('D5S818', 'D5S818'),
        ('D13S317', 'D13S317'), ('D7S820', 'D7S820'), ('D6S1043', 'D6S1043'),
        ('D10S1248', 'D10S1248'), ('D1S1656', 'D1S1656'), ('D12S391', 'D12S391'),
        ('D2S1338', 'D2S1338'), ('Penta', 'Penta')
    ]
    child = models.ForeignKey(Child, on_delete=models.PROTECT, null=True, blank=True)
    locus = models.CharField(max_length=10, choices=LOCUS, blank=True)
    data = models.CharField(max_length=10, blank=True)
