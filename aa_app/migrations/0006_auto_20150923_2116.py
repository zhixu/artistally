# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('aa_app', '0005_auto_20150923_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='users',
            field=models.ManyToManyField(related_name='conventions', default=None, blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
