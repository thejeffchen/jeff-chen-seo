# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-14 23:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0002_auto_20171014_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='dt_created',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]