# Generated by Django 3.0.1 on 2021-06-21 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0003_auto_20210621_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='relevantMedicine',
            field=models.ManyToManyField(blank=True, to='wall.Medicine'),
        ),
    ]
