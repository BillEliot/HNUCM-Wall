# Generated by Django 2.1.5 on 2019-10-19 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0044_user_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='openid',
            field=models.CharField(default=0, max_length=50),
        ),
    ]
