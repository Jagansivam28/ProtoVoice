# Generated by Django 2.2.5 on 2019-09-18 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verified',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
