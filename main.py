#!/usr/bin/env python3
import os.path
import subprocess
from pathlib import Path

from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def process():
    payload = request.json
    repository = payload["repository"]
    print(repository["full_name"])
    name = repository["name"]
    git_url = repository["git_url"]
    current_path = os.path.dirname(os.path.realpath(__file__))
    parent = Path(current_path).parent.absolute()
    app_path=os.path.join(parent,name)
    if not os.path.exists(app_path):
        os.chdir(parent)
        subprocess.run(["git",f"clone {git_url}"])
        os.chdir(app_path)
    else:
        os.chdir(app_path)
        subprocess.run(["git","pull"])
    if os.path.exists("run-me.sh"):
        subprocess.run(["run-me.sh"])
    return "Ok"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
