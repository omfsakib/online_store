# Generated by Django 3.2.7 on 2021-11-01 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_web', '0006_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rate',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
