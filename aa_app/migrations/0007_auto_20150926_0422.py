# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aa_app', '0006_auto_20150923_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='name',
            field=models.TextField(unique=True),
        ),
    ]
