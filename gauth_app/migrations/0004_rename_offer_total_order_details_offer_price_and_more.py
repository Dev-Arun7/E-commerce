# Generated by Django 4.2.7 on 2024-02-15 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gauth_app', '0003_order_details_delete_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order_details',
            old_name='offer_total',
            new_name='offer_price',
        ),
        migrations.AddField(
            model_name='order_details',
            name='quntity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
