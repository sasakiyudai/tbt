# Generated by Django 2.2.17 on 2021-07-25 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='github_url',
            field=models.TextField(blank=True, null=True, verbose_name='GitHubURL'),
        ),
    ]
