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
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('username', models.SlugField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('startYear', models.PositiveSmallIntegerField(default=None, null=True, blank=True)),
                ('image', models.URLField(default='', blank=True)),
                ('superuser', models.BooleanField(default=False)),
                ('description', models.TextField(default='', blank=True)),
                ('website1', models.URLField(default='', blank=True)),
                ('website2', models.URLField(default='', blank=True)),
                ('website3', models.URLField(default='', blank=True)),
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
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('numAttenders', models.PositiveIntegerField()),
                ('location', models.CharField(max_length=50)),
                ('website', models.URLField()),
                ('image', models.URLField(default='', blank=True)),
                ('prevCon', models.OneToOneField(null=True, blank=True, related_name='_nextCon', to='aa_app.Convention', default=None)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, default=None, blank=True, related_name='conventions')),
            ],
            options={
                'abstract': False,
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
                ('price', models.DecimalField(max_digits=10, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
                ('cost', models.DecimalField(max_digits=10, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
                ('numSold', models.PositiveIntegerField()),
                ('numLeft', models.PositiveIntegerField()),
                ('image', models.URLField(default='', blank=True)),
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
                ('amount', models.DecimalField(max_digits=10, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
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
