# Generated by Django 5.1 on 2024-09-10 21:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0011_delete_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
