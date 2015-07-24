# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aa_app', '0003_auto_20150717_0345'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.URLField(default=None, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.URLField(default=None, blank=True, null=True),
        ),
    ]
