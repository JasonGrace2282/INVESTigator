#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

import lorem

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
        "name": "Mystery of the Hat",
        "description": "\n".join((lorem.paragraph(), lorem.paragraph())),
    },
    {
        "lead": "Billy Bob",
        "name": "Mall Mystery",
        "description": "\n".join((lorem.paragraph(), lorem.paragraph())),
    },
    {
        "lead": "Geoffery Jack",
        "name": "Murder of the Cat",
        "description": lorem.paragraph(),
    }
]

for case_data in DATA:
    obj, created = Case.objects.get_or_create(**case_data)
    if not created:
        continue
    obj.save()
