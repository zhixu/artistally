# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aa_app', '0003_item_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='numAttenders',
            field=models.PositiveIntegerField(default=None, blank=True, null=True),
        ),
    ]
