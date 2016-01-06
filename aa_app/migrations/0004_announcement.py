# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-03 07:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aa_app', '0003_user_confirmtoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('message', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]