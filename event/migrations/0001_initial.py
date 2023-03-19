# Generated by Django 4.1.2 on 2023-03-19 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('detail', models.CharField(max_length=500)),
                ('organizer', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
                ('location', models.CharField(max_length=50)),
                ('is_completed', models.BooleanField(default=False)),
                ('is_live', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
