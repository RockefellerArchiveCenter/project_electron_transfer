# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-17 16:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0006_organization_testfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='testfil4e',
            field=models.CharField(default='', max_length=120),
            preserve_default=False,
        ),
    ]