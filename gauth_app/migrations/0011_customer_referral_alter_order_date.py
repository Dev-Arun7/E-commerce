# Generated by Django 4.2.7 on 2024-02-19 12:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gauth_app', '0010_order_details_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='referral',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
    ]