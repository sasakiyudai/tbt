# Generated by Django 2.2.17 on 2021-07-26 11:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0004_auto_20210723_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='images/', verbose_name='写真'),
            preserve_default=False,
        ),
    ]
