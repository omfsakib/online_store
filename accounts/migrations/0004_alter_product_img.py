# Generated by Django 3.2.7 on 2021-10-25 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20211025_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.ImageField(blank=True, default='product-pic.jpg', null=True, upload_to=''),
        ),
    ]