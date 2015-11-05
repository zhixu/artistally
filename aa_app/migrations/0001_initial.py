# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login', null=True)),
                ('username', models.SlugField(serialize=False, primary_key=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('superuser', models.BooleanField(default=False)),
                ('startYear', models.PositiveSmallIntegerField(blank=True, null=True, default=None)),
                ('image', models.URLField(blank=True, default='')),
                ('description', models.TextField(blank=True, default='')),
                ('website1', models.URLField(blank=True, default='')),
                ('website2', models.URLField(blank=True, default='')),
                ('website3', models.URLField(blank=True, default='')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Convention',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('website', models.URLField()),
                ('image', models.URLField(blank=True, default='')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('numAttenders', models.PositiveIntegerField(blank=True, null=True, default=None)),
                ('location', models.CharField(max_length=50)),
                ('convention', models.ForeignKey(to='aa_app.Convention', related_name='events')),
                ('users', models.ManyToManyField(related_name='events', blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'ordering': ['startDate'],
            },
        ),
        migrations.CreateModel(
            name='Fandom',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(max_digits=10, validators=[django.core.validators.MinValueValidator(0)], decimal_places=2)),
                ('cost', models.DecimalField(max_digits=10, validators=[django.core.validators.MinValueValidator(0)], decimal_places=2)),
                ('numSold', models.PositiveIntegerField()),
                ('numLeft', models.PositiveIntegerField()),
                ('image', models.URLField(blank=True, default='')),
                ('tag', models.UUIDField(blank=True, null=True, default=None)),
                ('event', models.ForeignKey(to='aa_app.Event', related_name='items')),
                ('fandom', models.ForeignKey(to='aa_app.Fandom', related_name='items')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Kind',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MiscCost',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('amount', models.DecimalField(max_digits=10, validators=[django.core.validators.MinValueValidator(0)], decimal_places=2)),
                ('name', models.CharField(max_length=50)),
                ('event', models.ForeignKey(to='aa_app.Event', related_name='miscCosts')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='miscCosts')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Writeup',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('review', models.TextField()),
                ('writeTime', models.DateTimeField(auto_now_add=True)),
                ('editTime', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(to='aa_app.Event', related_name='writeups')),
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
