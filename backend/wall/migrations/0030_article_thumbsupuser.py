# Generated by Django 2.1.5 on 2019-06-15 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0029_auto_20190613_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='thumbsUpUser',
            field=models.ManyToManyField(blank=True, related_name='user_thumbsUp', to='wall.User'),
        ),
    ]
