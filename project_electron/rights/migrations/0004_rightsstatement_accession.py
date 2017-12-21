# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-21 21:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accession', '0002_auto_20171220_2145'),
        ('rights', '0003_auto_20171207_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='rightsstatement',
            name='accession',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accession.Accession'),
        ),
    ]
