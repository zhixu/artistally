# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aa_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='website',
            field=models.URLField(default='website.com'),
            preserve_default=False,
        ),
    ]
