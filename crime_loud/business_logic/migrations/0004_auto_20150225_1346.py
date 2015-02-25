# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business_logic', '0003_auto_20150224_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdeattribute',
            name='digitalData',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
    ]
