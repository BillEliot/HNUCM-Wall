# Generated by Django 3.0.1 on 2020-04-11 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0054_bank_updatemessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='isAdopted',
            field=models.BooleanField(default=False),
        ),
    ]
