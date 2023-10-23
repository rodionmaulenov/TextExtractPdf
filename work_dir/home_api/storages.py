from storages.backends.s3boto3 import S3Boto3Storage


class MediaSpaceStorage(S3Boto3Storage):
    location = 'media'


class StaticSpaceStorage(S3Boto3Storage):
    location = 'static'
