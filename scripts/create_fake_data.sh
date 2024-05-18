#!/usr/bin/bash

python3 manage.py migrate

python3 create_fake_cases.py
