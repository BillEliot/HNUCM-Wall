# Generated by Django 2.1.5 on 2019-05-24 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0005_auto_20190524_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='love',
            name='comments',
            field=models.ManyToManyField(blank=True, to='wall.Comment'),
        ),
        migrations.AlterField(
            model_name='love',
            name='images',
            field=models.ManyToManyField(blank=True, to='wall.Image'),
        ),
    ]
