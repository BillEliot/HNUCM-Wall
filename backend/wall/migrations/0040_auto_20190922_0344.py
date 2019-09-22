# Generated by Django 2.1.5 on 2019-09-22 03:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0039_auto_20190921_0921'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('messageType', models.CharField(max_length=10)),
                ('messageFrom', models.CharField(max_length=10)),
                ('messageID', models.IntegerField()),
                ('commentContent', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wall.User')),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
        migrations.AlterModelOptions(
            name='lecture',
            options={'ordering': ('-date',)},
        ),
    ]
