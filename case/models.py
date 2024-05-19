from django.conf import settings
from django.db import models


class Case(models.Model):
    name = models.CharField(max_length=1024)
    description = models.CharField(blank=True, max_length=4096)
    lead = models.CharField(default="John Doe", max_length=512)

    def __str__(self):
        return f"{type(self).__name__} ({self.name})"


class Evidence(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="evidences",
    )

    email = models.EmailField(blank=True)
    text = models.TextField(blank=True, max_length=4096)
    image = models.ImageField(blank=True)
    video = models.FileField(blank=True)

    def __str__(self):
        return f"{type(self).__name__} for {self.case!s}"
