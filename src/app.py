from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/")
def hello():
    print('*' * 100)
    print(request.headers)
    print('*' * 100)
    return "Hello Kubernetes!"

