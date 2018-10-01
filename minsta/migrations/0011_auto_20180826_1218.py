# Generated by Django 2.0.6 on 2018-08-26 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('minsta', '0010_post_cafe'),
    ]

    operations = [
        migrations.AddField(
            model_name='cafe',
            name='area',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='cafe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='minsta.Cafe'),
        ),
    ]
