# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-11-12 16:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0049_initiative_instagram'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ('name',), 'verbose_name': 'Ciudad', 'verbose_name_plural': 'Ciudades'},
        ),
    ]
