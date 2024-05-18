# Generated by Django 5.0.6 on 2024-05-18 19:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0002_case_lead'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='evidence',
        ),
        migrations.AddField(
            model_name='evidence',
            name='image',
            field=models.ImageField(default=None, upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evidence',
            name='video',
            field=models.FileField(default=None, upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='case',
            name='description',
            field=models.CharField(blank=True, max_length=4096),
        ),
        migrations.AlterField(
            model_name='evidence',
            name='case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='case.case', verbose_name='evidences'),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.DeleteModel(
            name='Video',
        ),
    ]