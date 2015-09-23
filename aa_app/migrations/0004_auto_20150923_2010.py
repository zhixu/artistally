# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aa_app', '0003_auto_20150923_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='prevCon',
            field=models.OneToOneField(null=True, related_name='nextCon', default=None, to='aa_app.Convention', blank=True),
        ),
    ]
