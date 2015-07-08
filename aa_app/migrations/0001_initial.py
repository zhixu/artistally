# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Convention',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('numAttenders', models.PositiveIntegerField()),
                ('location', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Fandom',
            fields=[
                ('name', models.TextField(primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('cost', models.DecimalField(max_digits=10, decimal_places=2)),
                ('numSold', models.PositiveIntegerField()),
                ('numLeft', models.PositiveIntegerField()),
                ('convention', models.ForeignKey(to='aa_app.Convention', related_name='items')),
                ('fandom', models.ForeignKey(to='aa_app.Fandom', related_name='items')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Kind',
            fields=[
                ('name', models.TextField(primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.SlugField(primary_key=True, serialize=False)),
                ('password', models.TextField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('cookieID', models.BigIntegerField(unique=True)),
                ('startYear', models.PositiveSmallIntegerField(null=True, blank=True, default=None)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Writeup',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('review', models.TextField()),
                ('miscCosts', models.DecimalField(max_digits=10, decimal_places=2)),
                ('writeTime', models.DateTimeField(auto_now_add=True)),
                ('editTime', models.DateTimeField(auto_now=True)),
                ('convention', models.ForeignKey(to='aa_app.Convention', related_name='writeups')),
                ('user', models.ForeignKey(to='aa_app.User', related_name='writeups')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='item',
            name='kind',
            field=models.ForeignKey(to='aa_app.Kind', related_name='items'),
        ),
        migrations.AddField(
            model_name='item',
            name='user',
            field=models.ForeignKey(to='aa_app.User', related_name='items'),
        ),
    ]
