# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='caseAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caseName', models.CharField(max_length=30)),
                ('caseNumber', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='pdeAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=40)),
                ('date', models.DateTimeField()),
                ('digitalData', models.CharField(max_length=30)),
                ('photo', models.FileField(null=True, upload_to=b'photo')),
                ('video', models.FileField(null=True, upload_to=b'video')),
                ('audio', models.FileField(null=True, upload_to=b'audio')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('identity', models.CharField(max_length=13)),
                ('email', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('userRole', models.CharField(max_length=4)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pdeattribute',
            name='Person',
            field=models.ForeignKey(to='business_logic.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pdeattribute',
            name='caseAttribute',
            field=models.ForeignKey(to='business_logic.caseAttribute'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='caseattribute',
            name='person',
            field=models.ForeignKey(to='business_logic.Person'),
            preserve_default=True,
        ),
    ]
