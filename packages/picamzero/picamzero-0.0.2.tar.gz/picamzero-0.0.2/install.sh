#!/bin/bash
# Make the installation less painful
# until there is an apt package
set -euo pipefail

if [ "$(whoami)" = "root" ]; then
  echo "Do not run as root"
  exit 1
fi

echo "I will need to use sudo to install some dependencies"

sudo apt-get update
# put other deps here
sudo apt-get install -y python3-opencv python3-venv libcap-dev python3-libcamera
(cd "$HOME" && python3 -m venv --system-site-packages .picamzero-venv)
source "${HOME}/.picamzero-venv/bin/activate"
pip install list-of-python-deps..
