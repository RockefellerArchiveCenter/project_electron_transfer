# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-18 21:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bag_transfer', '0007_accession_process_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baginfometadata',
            name='record_type',
            field=models.CharField(max_length=256),
        ),
    ]