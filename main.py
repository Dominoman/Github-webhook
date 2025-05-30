#!/usr/bin/env python3
import logging
import os.path
import subprocess
from pathlib import Path

from flask import Flask, request

logging.basicConfig(filename="app.log", level=logging.INFO, format='%(asctime)s %(levelname)s : %(message)s')
app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_process():
    return 'Sabai sabai'


@app.route('/', methods=['POST'])
def post_process():
    if "X-GitHub-Event" not in request.headers:
        return 'Sabai sabai',404
    event = request.headers["X-GitHub-Event"]
    app.logger.info(event)
    if event != "push":
        return "Thanks"
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
        return "No master branch", 404
    current_path = os.path.dirname(os.path.realpath(__file__))
    parent = Path(current_path).parent.absolute()
    app_path = os.path.join(parent, name)
    if not os.path.exists(app_path):
        os.chdir(parent)
        git_url = repository["git_url"].replace("git://", "https://")
        app.logger.info(f"Cloning:{git_url} under {parent}")
        result = subprocess.run(["git", "clone", git_url], capture_output=True, text=True)
        app.logger.info(result.stdout)
        app.logger.error(result.stderr)
        os.chdir(app_path)
    else:
        os.chdir(app_path)
        app.logger.info(f"pulling under {app_path}")
        result = subprocess.run(["git", "pull"], capture_output=True, text=True)
        app.logger.info(result.stdout)
        app.logger.error(result.stderr)
    if os.path.exists("run-me.sh"):
        # os.chmod("run-me.sh",0o744)
        app.logger.info("Running run-me.sh")
        result = subprocess.run(["bash", "run-me.sh"], capture_output=True, text=True)
        app.logger.info(result.stdout)
        app.logger.error(result.stderr)
    app.logger.info("Done")
    return "Ok"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
