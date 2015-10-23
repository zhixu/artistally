# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aa_app', '0002_misccost_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='tag',
            field=models.UUIDField(null=True, default=None, blank=True),
        ),
    ]
