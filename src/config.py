import os


S3_INSTANCE_ROLE_BUCKET_NAME = os.environ.get('S3_INSTANCE_ROLE_BUCKET_NAME')
S3_POD_ROLE_BUCKET_NAME = os.environ.get('S3_POD_ROLE_BUCKET_NAME')
S3_CREDENTIALS_BUCKET_NAME = os.environ.get('S3_CREDENTIALS_BUCKET_NAME')
ENVIRONMENT = os.environ.get('ENVIRONMENT')

