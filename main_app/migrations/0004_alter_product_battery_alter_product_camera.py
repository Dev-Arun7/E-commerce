# Generated by Django 4.2.7 on 2024-02-09 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_brand_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='battery',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='camera',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]