# Generated by Django 2.0.3 on 2018-05-02 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0007_auto_20180502_2035'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='desination',
            new_name='destination',
        ),
    ]
