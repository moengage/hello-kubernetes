import os


S3_POD_ROLE_BUCKET_NAME = os.environ.get('S3_POD_ROLE_BUCKET_NAME')
ENVIRONMENT = os.environ.get('ENVIRONMENT')
SECRET_KEY = 'foo'
SECRET_VALUE = os.environ.get(SECRET_KEY)
