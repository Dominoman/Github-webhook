#!/bin/bash

cd "$(dirname "$0")"
set -ex

if [ ! -x ./.venv]; then
  python -m venv .venv
fi


