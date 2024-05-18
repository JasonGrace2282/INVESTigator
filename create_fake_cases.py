#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

if not __file__.endswith("shell.py"):
    subprocess.call(
        [
            sys.executable,
            Path(__file__).resolve().parent / "manage.py",
            "shell",
            "-c",
            open(__file__).read(),
        ]
    )
    exit()


from case.models import Case

DATA = [
    {
        "lead": "John Doe",
        "name": "Mystery of the missing hat",
        "description": "",
    },
    {
        "lead": "Billy Bob",
        "name": "Mall Mystery",
        "description": "",
    },
    {
        "lead": "Geoffery Jack",
        "name": "Murder of the Cat",
        "description": "",
    }
]

for case_data in DATA:
    obj, created = Case.objects.get_or_create(**case_data)
    if not created:
        continue
    obj.save()
