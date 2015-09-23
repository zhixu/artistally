# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aa_app', '0002_auto_20150923_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='prevCon',
            field=models.ForeignKey(related_name='nextCon', blank=True, default=None, null=True, to='aa_app.Convention'),
        ),
    ]
