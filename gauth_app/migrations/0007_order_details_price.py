# Generated by Django 4.2.7 on 2024-02-15 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gauth_app', '0006_order_details_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_details',
            name='price',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
