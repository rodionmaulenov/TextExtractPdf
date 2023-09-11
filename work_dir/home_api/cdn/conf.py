import os

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = 'text-extract-pdf-spaces'
AWS_S3_ENDPOINT_URL = "https://fra1.digitaloceanspaces.com"
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
    "ACL": "public-read"
}
AWS_LOCATION = "https://text-extract-pdf-spaces.fra1.digitaloceanspaces.com"
DEFAULT_FILE_STORAGE = "home_api.cdn.backends.MediaRootS3BotoStorage"
STATICFILES_STORAGE = 'home_api.cdn.backends.StaticRootS3BotoStorage'