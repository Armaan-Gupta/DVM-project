# Generated by Django 4.2 on 2023-05-13 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_vendor',
            field=models.BooleanField(default=False),
        ),
    ]
