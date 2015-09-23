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
            name='prevCon',
            field=models.ForeignKey(related_name='nextCon', blank=True, null=True, to='aa_app.Convention'),
        ),
        migrations.AlterField(
            model_name='convention',
            name='image',
            field=models.URLField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.URLField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.URLField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='website1',
            field=models.URLField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='website2',
            field=models.URLField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='website3',
            field=models.URLField(default='', blank=True),
        ),
    ]
