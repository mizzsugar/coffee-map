# Generated by Django 2.0.6 on 2018-06-23 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minsta', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='posted_at',
            field=models.DateField(auto_now=True),
        ),
    ]