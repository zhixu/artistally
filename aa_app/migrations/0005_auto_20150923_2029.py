# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('aa_app', '0004_auto_20150923_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='users',
            field=models.ManyToManyField(related_name='conventions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='convention',
            name='prevCon',
            field=models.OneToOneField(default=None, related_name='_nextCon', blank=True, null=True, to='aa_app.Convention'),
        ),
    ]
