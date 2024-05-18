from django.contrib import admin

from .models import Case, Evidence

models = [
    Case,
    Evidence,
]

for m in models:
    admin.site.register(m)
