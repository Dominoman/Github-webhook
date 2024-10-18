#!/bin/bash

cd "$(dirname "$0")"
set -ex

# Virtuális környezet létrehozása
if [ ! -f pyvenv.cfg ] ; then
  python -m venv .
fi

# Aktiváljuk a virtuális környezetet
source bin/activate

# Csomagok installálása
if [ -f requirements.txt ] ; then
  pip install -r requirements.txt
fi

currentpath=$(pwd)
username=$(whoami)
groupname=$(id -gn)
servicename="github-webhook"

if [ ! -f $servicename.service ] ; then
  cp $servicename.service.template $servicename.service
  sed -i "s|%currentpath%|$currentpath|g; s|%username%|$username|g; s|%groupname%|$groupname|g" $servicename.service
fi

if [ ! -f /etc/systemd/system/$servicename.service ] ; then
  sudo ln -s "$currentpath/$servicename.service" /etc/systemd/system/$servicename.service
fi

# Restart gunicorn
sudo systemctl daemon-reload
sudo systemctl enable $servicename
sudo systemctl restart $servicename

deactivate
