# Generated by Django 3.1.1 on 2020-09-26 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='image',
        ),
        migrations.AddField(
            model_name='listing',
            name='image_url',
            field=models.URLField(blank=True),
        ),
    ]