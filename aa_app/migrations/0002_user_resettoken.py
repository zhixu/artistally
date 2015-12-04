# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aa_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='resetToken',
            field=models.UUIDField(null=True, default=None, blank=True),
        ),
    ]
