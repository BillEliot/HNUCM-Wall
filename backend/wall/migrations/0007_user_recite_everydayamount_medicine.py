# Generated by Django 3.0.1 on 2021-06-30 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0006_auto_20210628_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='recite_everydayAmount_medicine',
            field=models.IntegerField(default=0),
        ),
    ]