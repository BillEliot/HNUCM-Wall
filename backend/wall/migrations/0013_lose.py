# Generated by Django 2.1.5 on 2019-05-30 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0012_user_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lose',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isFound', models.BooleanField(default=False)),
                ('date', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('images', models.ManyToManyField(blank=True, to='wall.Image')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]