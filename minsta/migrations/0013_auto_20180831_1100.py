# Generated by Django 2.0.6 on 2018-08-31 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minsta', '0012_forgetpassworduser_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forgetpassworduser',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]