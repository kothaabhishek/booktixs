#!/usr/bin/env bash
set -o errexit

"${PYTHON:-python3}" manage.py collectstatic --noinput
