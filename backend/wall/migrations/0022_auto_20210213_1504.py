# Generated by Django 3.1.6 on 2021-02-13 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0021_auto_20210213_1502'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='losee',
            new_name='lose',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='lovee',
            new_name='love',
        ),
    ]