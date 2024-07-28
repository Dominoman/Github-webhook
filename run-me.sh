#!/bin/bash


cd "$(dirname "$0")"
set -ex

# Virtuális környezet létrehozása
if [ ! -x .venv ] ; then
  python -m venv .venv
fi

# Aktiváljuk a virtuális környezetet
source .venv/bin/activate

# Csomagok installálása
if [ -f requirements.txt ] ; then
  pip install -r requirements.txt
fi

if [ ! -f github-webhook.service ] ; then
  cp github-webhook.service.template github-webhook.service
fi
currentpath=$(pwd)
sed -i "s|%currentpath%|$currentpath|g" github-webhook.service

if [ ! -f /etc/systemd/system/github-webhook.service ] ; then
  sudo ln -s "$currentpath/github-webhook.service" /etc/systemd/system/github-webhook.service
fi

# Restart gunicorn
sudo systemctl daemon-reload
sudo systemctl enable github-webhook
sudo systemctl restart github-webhook

deactivate