# Generated by Django 3.1.6 on 2021-02-10 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0011_auto_20210210_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='lecturerInfo',
            field=models.TextField(null=True),
        ),
    ]