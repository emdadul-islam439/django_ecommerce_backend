# Generated by Django 4.1.5 on 2023-01-12 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0004_remove_shippingaddress_order_order_shipping_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_shipped',
            field=models.BooleanField(default=False),
        ),
    ]
