#!/usr/bin/env python3
import logging
import os.path
import subprocess
from pathlib import Path

from flask import Flask, request

logging.basicConfig(filename="app.log",level=logging.INFO)
app = Flask(__name__)


@app.route('/', methods=['POST'])
def process():
    payload = request.json
    repository = payload["repository"]
    app.logger.info(f"Repository:{repository['full_name']}")
    name = repository["name"]
    head_commit = payload["head_commit"]
    app.logger.info(f"Message:{head_commit['message']}")
    branch = payload["ref"].split('/')[-1]
    master_branch = repository["master_branch"]
    if branch != master_branch:
        app.logger.info("Skipped - no master branch")
        return
    current_path = os.path.dirname(os.path.realpath(__file__))
    parent = Path(current_path).parent.absolute()
    app_path = os.path.join(parent, name)
    if not os.path.exists(app_path):
        os.chdir(parent)
        git_url = repository["git_url"]
        subprocess.run(["git", f"clone {git_url}"])
        os.chdir(app_path)
    else:
        os.chdir(app_path)
        subprocess.run(["git", "pull"])
    if os.path.exists("run-me.sh"):
        subprocess.run(["bash","run-me.sh"])
    return "Ok"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
