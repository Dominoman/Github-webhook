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
  currentpath=$(pwd)
  sed -i "s|%currentpath%|$currentpath|g" github-webhook.service
fi

# Restart gunicorn
sudo systemctl restart gunicorn

deactivate