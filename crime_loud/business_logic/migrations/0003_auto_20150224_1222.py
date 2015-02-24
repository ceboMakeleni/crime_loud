# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business_logic', '0002_person_cell_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdeattribute',
            name='caseAttribute',
            field=models.ForeignKey(to='business_logic.caseAttribute', null=True),
            preserve_default=True,
        ),
    ]
