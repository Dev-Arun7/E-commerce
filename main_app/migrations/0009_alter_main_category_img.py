# Generated by Django 4.2.7 on 2023-11-17 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_alter_main_category_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='main_category',
            name='img',
            field=models.ImageField(default='categories/default_image.jpg', null=True, upload_to='categories'),
        ),
    ]