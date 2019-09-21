# Generated by Django 2.1.5 on 2019-09-21 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0038_lecture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Help',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comments', models.ManyToManyField(blank=True, to='wall.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wall.User')),
            ],
        ),
        migrations.AlterField(
            model_name='lecture',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
