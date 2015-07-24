# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aa_app', '0004_auto_20150722_0042'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='image',
            field=models.URLField(blank=True, default=None, null=True),
        ),
    ]
