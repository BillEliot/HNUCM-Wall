# Generated by Django 3.0.1 on 2020-01-08 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0052_auto_20200107_2058'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ('-publicDate',)},
        ),
        migrations.AlterModelOptions(
            name='deal',
            options={'ordering': ('-date',)},
        ),
        migrations.AlterModelOptions(
            name='help',
            options={'ordering': ('-date',)},
        ),
        migrations.AlterModelOptions(
            name='hot',
            options={'ordering': ('-date',)},
        ),
        migrations.AlterModelOptions(
            name='lose',
            options={'ordering': ('-publicDate',)},
        ),
        migrations.AlterModelOptions(
            name='love',
            options={'ordering': ('-date',)},
        ),
        migrations.AlterField(
            model_name='bank',
            name='answer',
            field=models.TextField(),
        ),
    ]