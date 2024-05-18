#!/usr/bin/bash

python3 manage.py migrate

echo "Creating fake data"
python3 create_fake_cases.py

python3 scripts/create_superuser.py
