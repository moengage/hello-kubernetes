
import json
import signal
import os
import time

import boto3
from botocore.exceptions import ClientError
from flask import Flask
from flask import request, render_template, jsonify

from src.config import (S3_POD_ROLE_BUCKET_NAME, ENVIRONMENT, SECRET_KEY, SECRET_VALUE)


def load_config(fail_silently=True, *args, **kwargs):
    config_path = '/opt/hola/dynamic-config.json'

    retry = 60
    for i in range(retry):
        try:
            with open(config_path) as fp:
                app.dynamic_config = json.load(fp)
        except FileNotFoundError:
            time.sleep(1)
            print('Retrying fetching config!')
            if i+1 == retry:
                print('Failed to load config.')
                if fail_silently:
                    print('Failing silently.')
                    app.dynamic_config = {}
                else:
                    raise


app = Flask(__name__)
load_config(fail_silently=False)
signal.signal(signal.SIGUSR1, load_config)


@app.route("/")
def hola():
    template = (
        "Hostname: {pod_name}\n"
        "Namespace: {pod_namespace}\n"
        "Environment: {environment}\n"
        "IP: {pod_ip}\n"
        "{request_method} {request_path} {http_version}\n"
        "Value of {secret_key} is {secret_value}\n"
        "Hello World!\n"
        "Dynamic config: {dynamic_config}\n"
    )

    pod_details = template.format(
        pod_name=os.getenv('POD_NAME'),
        pod_namespace=os.getenv('POD_NAMESPACE'),
        environment=ENVIRONMENT,
        pod_ip=os.getenv('POD_IP'),
        request_method=request.method,
        request_path=request.path,
        http_version=request.environ.get('SERVER_PROTOCOL'),
        secret_key=SECRET_KEY,
        secret_value=SECRET_VALUE,
        dynamic_config=app.dynamic_config
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

