# Generated by Django 2.1.5 on 2020-07-22 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0058_auto_20200722_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity_jingui',
            name='cover',
            field=models.ImageField(default='img/JinGui/default.png', upload_to='img/JinGui'),
        ),
    ]