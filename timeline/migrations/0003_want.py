# Generated by Django 2.2.17 on 2021-07-22 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timeline', '0002_post_station'),
    ]

    operations = [
        migrations.CreateModel(
            name='Want',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wanted', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wanted', to=settings.AUTH_USER_MODEL)),
                ('wanting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wanting', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('wanting', 'wanted')},
            },
        ),
    ]