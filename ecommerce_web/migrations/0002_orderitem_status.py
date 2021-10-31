# Generated by Django 3.2.7 on 2021-10-29 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered')], default='Pending', max_length=200, null=True),
        ),
    ]
