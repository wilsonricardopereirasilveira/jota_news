#!/bin/bash
set -euo pipefail

source infrastructure/scripts/load_env.sh

python manage.py migrate
