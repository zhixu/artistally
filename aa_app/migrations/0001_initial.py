# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('username', models.SlugField(serialize=False, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('startYear', models.PositiveSmallIntegerField(default=None, blank=True, null=True)),
                ('image', models.URLField(default=None, blank=True, null=True)),
                ('superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Convention',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('numAttenders', models.PositiveIntegerField()),
                ('location', models.TextField()),
                ('website', models.URLField()),
                ('image', models.URLField(default=None, blank=True, null=True)),
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
                ('image', models.URLField(default=None, blank=True, null=True)),
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
            name='MiscCost',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('convention', models.ForeignKey(to='aa_app.Convention', related_name='miscCosts')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='miscCosts')),
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
                ('writeTime', models.DateTimeField(auto_now_add=True)),
                ('editTime', models.DateTimeField(auto_now=True)),
                ('convention', models.ForeignKey(to='aa_app.Convention', related_name='writeups')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='writeups')),
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
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='items'),
        ),
    ]
