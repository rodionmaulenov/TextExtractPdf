# Generated by Django 4.2.4 on 2023-08-06 20:04

from django.db import migrations, models
import upload_file.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientExtractLocus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('locus', models.JSONField(blank=True, null=True)),
                ('file_upload', models.FileField(upload_to=upload_file.models.user_directory_path)),
            ],
        ),
    ]
