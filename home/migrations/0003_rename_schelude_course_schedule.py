# Generated by Django 3.2.9 on 2021-11-29 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_userprofile_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='schelude',
            new_name='schedule',
        ),
    ]
