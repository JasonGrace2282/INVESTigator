from pathlib import Path

from django.core.exceptions import ValidationError
from django.db import models


class Case(models.Model):
    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=4096)


class Evidence(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE
    )

    # for contacting user
    email = models.EmailField(blank=True)


class Image(models.Model):
    evidence = models.ForeignKey(
        Evidence,
        on_delete=models.CASCADE
    )

    image = models.ImageField()


def validate_video(value):
    path = Path(value.name)
    allowed = {"mp4", "mov"}
    if not path.suffix in allowed:
        raise ValidationError(f"Only files in {allowed} are allowed")


class Video(models.Model):
    evidence = models.ForeignKey(
        Evidence,
        on_delete=models.CASCADE
    )

    video = models.FileField()

