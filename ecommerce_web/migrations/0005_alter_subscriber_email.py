# Generated by Django 3.2.7 on 2021-10-30 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_web', '0004_mailmessage_subscriber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
