# Generated by Django 2.2.3 on 2019-07-29 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvals',
            name='is_authorized',
            field=models.BooleanField(default=False),
        ),
    ]
