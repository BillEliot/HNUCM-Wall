# Generated by Django 2.1.5 on 2019-05-30 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0013_lose'),
    ]

    operations = [
        migrations.AddField(
            model_name='lose',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wall.User'),
        ),
    ]
