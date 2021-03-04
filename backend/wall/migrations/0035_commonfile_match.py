# Generated by Django 3.1.6 on 2021-02-23 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0034_bank_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommonFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('_file', models.FileField(upload_to='file/')),
                ('_type', models.CharField(choices=[('word', 'word'), ('excel', 'excel'), ('ppt', 'ppt'), ('pdf', 'pdf')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('startDate', models.DateTimeField()),
                ('endDate', models.DateTimeField()),
                ('totalBonus', models.IntegerField()),
            ],
            options={
                'ordering': ('-startDate',),
            },
        ),
    ]