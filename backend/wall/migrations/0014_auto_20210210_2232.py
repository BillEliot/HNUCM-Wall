# Generated by Django 3.1.6 on 2021-02-10 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0013_auto_20210210_1821'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BankStatistics',
            new_name='Bank_Statistics',
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='state',
        ),
    ]
