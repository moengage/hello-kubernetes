import os

import boto3
from flask import Flask
from flask import request, render_template

from src.config import S3_BUCKET_NAME

app = Flask(__name__)


@app.route("/")
def hola():
    template = (
        "Hostname: {pod_name}\n"
        "Namespace: {pod_namespace}\n"
        "IP: {pod_ip}\n"
        "{request_method} {request_path} {http_version}\n"
    )
    pod_details = template.format(
        pod_name=os.getenv('POD_NAME'),
        pod_namespace=os.getenv('POD_NAMESPACE'),
        pod_ip=os.getenv('POD_IP'),
        request_method=request.method,
        request_path=request.path,
        http_version=request.environ.get('SERVER_PROTOCOL')
    )
    context = ''.join([pod_details, str(request.headers)])
    return render_template('template.html', context=context)


@app.route("/s3/")
def list_s3():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(S3_BUCKET_NAME)

    for object_summary in bucket.objects.filter(Prefix="/"):
        print(object_summary.key)

    return S3_BUCKET_NAME

