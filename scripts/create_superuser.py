import subprocess
import sys
from pathlib import Path

from django.contrib.auth import get_user_model

if not __file__.endswith("shell.py"):
    subprocess.call(
        [
            sys.executable,
            Path(__file__).resolve().parent.parent / "manage.py",
            "shell",
            "-c",
            open(__file__).read(),
        ]
    )
    exit()


User = get_user_model()

if not User.objects.filter(username="admin").exists():
    username = "admin"
    User.objects.create_superuser(username, "admin@gmail.com", input("Enter an admin password: "))
    print(f"Created admin account with {username = }")
