# Generated by Django 5.0.6 on 2024-05-18 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0003_remove_video_evidence_evidence_image_evidence_video_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evidence',
            name='text',
            field=models.TextField(blank=True, max_length=4096),
        ),
    ]