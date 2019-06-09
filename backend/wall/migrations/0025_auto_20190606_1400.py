# Generated by Django 2.1.5 on 2019-06-06 14:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0024_auto_20190603_1531'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lose',
            old_name='date',
            new_name='publicDate',
        ),
        migrations.AddField(
            model_name='lose',
            name='loseDate',
            field=models.CharField(default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
    ]
