# Generated by Django 4.2.7 on 2024-02-20 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_alter_banner_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='main_category',
            name='offer',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]