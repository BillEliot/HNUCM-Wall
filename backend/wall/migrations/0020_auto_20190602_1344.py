# Generated by Django 2.1.5 on 2019-06-02 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0019_auto_20190602_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='bank',
            field=models.CharField(max_length=20),
        ),
    ]