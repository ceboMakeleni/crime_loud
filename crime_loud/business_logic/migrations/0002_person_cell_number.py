# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business_logic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='cell_number',
            field=models.CharField(default=b'', max_length=10),
            preserve_default=True,
        ),
    ]
