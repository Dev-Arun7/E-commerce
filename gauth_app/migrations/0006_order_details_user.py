# Generated by Django 4.2.7 on 2024-02-15 09:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gauth_app', '0005_rename_quntity_order_details_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_details',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
