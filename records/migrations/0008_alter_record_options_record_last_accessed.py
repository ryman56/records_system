# Generated by Django 5.1 on 2024-09-05 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0007_remove_record_content'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='record',
            options={'ordering': ['title']},
        ),
        migrations.AddField(
            model_name='record',
            name='last_accessed',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
