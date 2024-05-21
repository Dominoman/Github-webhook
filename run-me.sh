#!/bin/bash

cd "$(dirname "$0")"
set -ex

# Csinálunk python virtuáis környezetet, ha nincs
if [ ! -x .venv ] ; then
  python -m venv .venv
fi

# Aktiváljuk a virtuális környezetet
source .venv/bin/activate

# Csomagok installálása
if [ -f requirements.txt ] ; then
  pip install -r requirements.txt
fi

