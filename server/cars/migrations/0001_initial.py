# Generated by Django 2.2.3 on 2019-07-29 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Approvals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('license_number', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=100)),
                ('picture', models.TextField()),
            ],
        ),
    ]
