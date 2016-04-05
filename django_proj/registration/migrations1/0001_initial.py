# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-31 18:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=10)),
                ('middle_name', models.CharField(max_length=10)),
                ('last_name', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=25, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('mobile_no', models.CharField(max_length=12)),
                ('admin_approval', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]