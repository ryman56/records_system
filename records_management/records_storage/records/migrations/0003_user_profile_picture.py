# Generated by Django 5.1 on 2024-09-03 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0002_remove_department_secret_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='profile_pics/'),
        ),
    ]
