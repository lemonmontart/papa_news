# Generated by Django 2.2.4 on 2024-01-16 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('keyword', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('press', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
