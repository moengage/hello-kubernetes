import os

import boto3
from botocore.exceptions import ClientError
from flask import Flask
from flask import request, render_template

from src.config import (S3_INSTANCE_ROLE_BUCKET_NAME, S3_POD_ROLE_BUCKET_NAME,
        S3_CREDENTIALS_BUCKET_NAME, ENVIRONMENT)

app = Flask(__name__)


@app.route("/")
def hola():
    template = (
        "Hostname: {pod_name}\n"
        "Namespace: {pod_namespace}\n"
        "Environment: {environment}\n"
        "IP: {pod_ip}\n"
        "{request_method} {request_path} {http_version}\n"
    )
    pod_details = template.format(
        pod_name=os.getenv('POD_NAME'),
        pod_namespace=os.getenv('POD_NAMESPACE'),
        environment=ENVIRONMENT,
        pod_ip=os.getenv('POD_IP'),
        request_method=request.method,
        request_path=request.path,
        http_version=request.environ.get('SERVER_PROTOCOL')
    )
    context = ''.join([pod_details, str(request.headers)])
    return render_template('template.html', context=context)


class S3Utils(object):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self._resource = boto3.resource('s3')
        self._bucket = self._resource.Bucket(self.bucket_name)

    def get_objects(self):
        data = []
        try:
            for object_summary in self._bucket.objects.all():
                data.append(object_summary.key)
            return data
        except ClientError as e:
            return [str(e)]


S3_LIST_OBJECTS_TEMPLATE = (
    '{role_type} access test\n'
    'Bucket Name: {bucket_name}\n'
    'Environment: {environment}\n'
    'S3 Objects (max 5 objects): {objects}\n'
)

@app.route("/s3-instance-role/")
def list_s3_instance_role():
    bucket = S3_INSTANCE_ROLE_BUCKET_NAME
    s3 = S3Utils(bucket)
    s3_objects = '   '.join(s3.get_objects()[:5])
    context = S3_LIST_OBJECTS_TEMPLATE.format(
        role_type='Instance role',
        bucket_name=bucket,
        environment=ENVIRONMENT,
        objects=s3_objects
    )
    return render_template('template.html', context=context)


@app.route("/s3-pod-role/")
def list_s3_pod_role():
    bucket = S3_POD_ROLE_BUCKET_NAME
    s3 = S3Utils(bucket)
    s3_objects = '   '.join(s3.get_objects()[:5])
    context = S3_LIST_OBJECTS_TEMPLATE.format(
        role_type='Pod role',
        bucket_name=bucket,
        environment=ENVIRONMENT,
        objects=s3_objects
    )
    return render_template('template.html', context=context)


@app.route("/s3-credentials/")
def list_s3():
    bucket = S3_CREDENTIALS_BUCKET_NAME
    s3 = S3Utils(bucket)
    s3_objects = '   '.join(s3.get_objects()[:5])
    context = S3_LIST_OBJECTS_TEMPLATE.format(
        role_type='Credentials',
        bucket_name=bucket,
        environment=ENVIRONMENT,
        objects=s3_objects
    )
    return render_template('template.html', context=context)

