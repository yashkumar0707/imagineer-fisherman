# Generated by Django 2.1.3 on 2020-03-08 00:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200308_0014'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sales',
            old_name='date',
            new_name='ds',
        ),
        migrations.RenameField(
            model_name='sales',
            old_name='qty',
            new_name='y',
        ),
    ]
