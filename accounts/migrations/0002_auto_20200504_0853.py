# Generated by Django 2.2.12 on 2020-05-04 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='rp_otp',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
