# Generated by Django 3.0.1 on 2020-01-04 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0050_bankresult'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BankResult',
            new_name='BankStatistics',
        ),
    ]
