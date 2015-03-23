# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_auto_20150323_0104'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='auth',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
    ]
