# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competicio', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='competicio',
            old_name='competicio_imatge',
            new_name='imatge',
        ),
        migrations.RenameField(
            model_name='competicio',
            old_name='competicio_text',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='prova',
            old_name='prova_date',
            new_name='datainici',
        ),
        migrations.RenameField(
            model_name='prova',
            old_name='prova_intents',
            new_name='intents',
        ),
        migrations.RenameField(
            model_name='prova',
            old_name='prova_resposta',
            new_name='resposta',
        ),
        migrations.RenameField(
            model_name='prova',
            old_name='prova_text',
            new_name='titol',
        ),
        migrations.RemoveField(
            model_name='prova',
            name='prova_titol',
        ),
        migrations.AddField(
            model_name='prova',
            name='text',
            field=models.TextField(default=b'prova'),
        ),
    ]
