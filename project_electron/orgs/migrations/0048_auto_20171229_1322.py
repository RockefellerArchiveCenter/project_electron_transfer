# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-29 18:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0047_auto_20171228_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acceptbagitversion',
            name='name',
            field=models.DecimalField(choices=[(0.96, 0.96), (0.97, 0.97)], decimal_places=2, max_digits=5),
        ),
    ]