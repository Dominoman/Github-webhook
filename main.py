#!/usr/bin/env python3
import os.path

from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def process():
    current_path = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(os.path.realpath(os.path.join(current_path,'..')))
    print(parent)
    payload = request.json
    repository = payload["repository"]
    print(repository["full_name"])
    print(current_path)
    name = repository["name"]

    return "Ok"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
