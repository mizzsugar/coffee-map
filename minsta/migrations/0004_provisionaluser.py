# Generated by Django 2.0.6 on 2018-08-05 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minsta', '0003_post_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProvisionalUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.TextField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
