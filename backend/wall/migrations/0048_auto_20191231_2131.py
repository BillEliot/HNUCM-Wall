# Generated by Django 3.0.1 on 2019-12-31 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0047_bank_subject_subjecttype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bank',
            old_name='bank',
            new_name='chapter',
        ),
    ]