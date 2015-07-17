# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def forwards_func(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Writeup = apps.get_model("aa_app", "Writeup")
    MiscCost = apps.get_model("aa_app", "MiscCost")
    for w in Writeup.objects.using(db_alias):
        m = MiscCost(user = w.user, convention = w.convention, amount = w.miscCosts)
        m.save(using = db_alias)

class Migration(migrations.Migration):

    dependencies = [
        ('aa_app', '0002_convention_website'),
    ]

    operations = [
        migrations.CreateModel(
            name='MiscCost',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('convention', models.ForeignKey(related_name='miscCosts', to='aa_app.Convention')),
                ('user', models.ForeignKey(related_name='miscCosts', to='aa_app.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        
        migrations.RunPython(
            forwards_func,
        ),
        
        migrations.RemoveField(
            model_name='writeup',
            name='miscCosts',
        ),
    ]
