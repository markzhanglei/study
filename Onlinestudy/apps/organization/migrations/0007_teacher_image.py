# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-05-06 00:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_auto_20180505_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='teacher/%Y/%m', verbose_name='教师图像'),
        ),
    ]
