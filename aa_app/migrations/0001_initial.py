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
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('username', models.SlugField(primary_key=True, serialize=False)),
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
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('website', models.URLField()),
                ('image', models.URLField(blank=True, default='')),
                ('users', models.ManyToManyField(related_name='conventions', blank=True, to=settings.AUTH_USER_MODEL, default=None)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('numAttenders', models.PositiveIntegerField()),
                ('location', models.CharField(max_length=50)),
                ('convention', models.ForeignKey(related_name='events', to='aa_app.Convention')),
            ],
            options={
                'ordering': ['startDate'],
            },
        ),
        migrations.CreateModel(
            name='Fandom',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('numSold', models.PositiveIntegerField()),
                ('numLeft', models.PositiveIntegerField()),
                ('image', models.URLField(blank=True, default='')),
                ('event', models.ForeignKey(related_name='items', to='aa_app.Event')),
                ('fandom', models.ForeignKey(related_name='items', to='aa_app.Fandom')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Kind',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MiscCost',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('event', models.ForeignKey(related_name='miscCosts', to='aa_app.Event')),
                ('user', models.ForeignKey(related_name='miscCosts', to=settings.AUTH_USER_MODEL)),
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
                ('event', models.ForeignKey(related_name='writeups', to='aa_app.Event')),
                ('user', models.ForeignKey(related_name='writeups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='item',
            name='kind',
            field=models.ForeignKey(related_name='items', to='aa_app.Kind'),
        ),
        migrations.AddField(
            model_name='item',
            name='user',
            field=models.ForeignKey(related_name='items', to=settings.AUTH_USER_MODEL),
        ),
    ]
