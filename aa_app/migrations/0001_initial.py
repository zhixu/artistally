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
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.TextField()),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('numAttenders', models.PositiveIntegerField()),
                ('location', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Fandom',
            fields=[
                ('name', models.TextField(serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('numSold', models.PositiveIntegerField()),
                ('numLeft', models.PositiveIntegerField()),
                ('convention', models.ForeignKey(related_name='items', to='aa_app.Convention')),
                ('fandom', models.ForeignKey(related_name='items', to='aa_app.Fandom')),
            ],
        ),
        migrations.CreateModel(
            name='Kind',
            fields=[
                ('name', models.TextField(serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.SlugField(primary_key=True, serialize=False)),
                ('password', models.TextField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('cookieID', models.BigIntegerField(unique=True)),
                ('startYear', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Writeup',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('review', models.TextField()),
                ('miscCosts', models.DecimalField(decimal_places=2, max_digits=10)),
                ('writeTime', models.DateTimeField(auto_now_add=True)),
                ('editTime', models.DateTimeField(auto_now=True)),
                ('convention', models.ForeignKey(related_name='writeups', to='aa_app.Convention')),
                ('user', models.ForeignKey(related_name='writeups', to='aa_app.User')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='kind',
            field=models.ForeignKey(related_name='items', to='aa_app.Kind'),
        ),
        migrations.AddField(
            model_name='item',
            name='user',
            field=models.ForeignKey(related_name='items', to='aa_app.User'),
        ),
    ]
