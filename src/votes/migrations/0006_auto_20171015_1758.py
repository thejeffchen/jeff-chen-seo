# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-16 00:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0005_auto_20171014_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(upload_to=''),
        ),
    ]