# Generated by Django 3.2.9 on 2021-11-29 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_delete_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(null=True, verbose_name='Giới thiệu bản thân'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birthday',
            field=models.DateField(null=True, verbose_name='Ngày sinh'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='department',
            field=models.CharField(max_length=100, null=True, verbose_name='Nơi công tác'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.BooleanField(choices=[(True, 'Nam'), (False, 'Nữ')], null=True, verbose_name='Giới tính'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_teacher',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profession',
            field=models.CharField(max_length=50, null=True, verbose_name='Nghề nghiệp'),
        ),
    ]
