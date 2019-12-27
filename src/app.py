import os

from flask import Flask
from flask import request, render_template


app = Flask(__name__)


@app.route("/")
def hello():
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
