from wsgiref.simple_server import make_server
from flask import Flask

app = Flask(__name__)


@app.route('/')
def start():
    return 'Hello World'


@app.route('/api/v1/hello-world-2')
def hello_world():
    return 'Hello World 2'


with make_server('', 8080, app) as server:
    print("Something http://127.0.0.1:8080")
    print("Something http://127.0.0.1:8080/api/v1/hello-world-2")
    server.serve_forever()
