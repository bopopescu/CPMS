# Generated by Django 2.1.1 on 2018-10-05 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0012_profile_ugs'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='ugs',
            new_name='ug_stream',
        ),
    ]
