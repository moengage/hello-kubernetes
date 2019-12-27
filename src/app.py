import os

from flask import Flask
from flask import request


app = Flask(__name__)


@app.route("/")
def hello():
    template = """
    Hostname: {pod_name}
    Namespace: {pod_namespace}
    IP: {pod_ip}
    {request_method} {request_path} {http_version}
    """
    response = template.format(
            pod_name=os.getenv('POD_NAME'),
            pod_namespace=os.getenv('POD_NAMESPACE'),
            pod_ip=os.getenv('POD_IP'),
            request_method=request.method,
            request_path=request.path,
            http_version=request.environ.get('SERVER_PROTOCOL'))
    return '\n'.join([response, str(request.headers)])

