# Generated by Django 2.2.17 on 2021-07-15 10:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='station',
            field=models.TextField(default=django.utils.timezone.now, verbose_name='場所'),
            preserve_default=False,
        ),
    ]
