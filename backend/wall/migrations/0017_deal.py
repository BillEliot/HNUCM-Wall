# Generated by Django 2.1.5 on 2019-05-31 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0016_lose_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isSold', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=20)),
                ('price', models.FloatField()),
                ('new', models.IntegerField()),
                ('description', models.TextField()),
                ('comments', models.ManyToManyField(blank=True, to='wall.Comment')),
                ('images', models.ManyToManyField(blank=True, to='wall.Image')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wall.User')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]