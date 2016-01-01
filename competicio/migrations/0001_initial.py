# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competicio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('competicio_text', models.CharField(max_length=200)),
                ('competicio_imatge', models.ImageField(default=b'images/none.png', upload_to=b'images/')),
            ],
        ),
        migrations.CreateModel(
            name='Prova',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prova_titol', models.CharField(max_length=200)),
                ('prova_text', models.CharField(max_length=200)),
                ('prova_resposta', models.CharField(max_length=200)),
                ('prova_date', models.DateTimeField(verbose_name=b'date published')),
                ('prova_intents', models.BigIntegerField()),
                ('competicio', models.ForeignKey(to='competicio.Competicio')),
            ],
        ),
    ]
