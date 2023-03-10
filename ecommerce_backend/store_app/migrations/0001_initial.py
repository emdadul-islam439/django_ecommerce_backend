# Generated by Django 4.1.5 on 2023-01-03 18:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=200, null=True)),
                ('image', models.ImageField(default='default.png', upload_to='profile_pics')),
                ('user', models.OneToOneField(default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.IntegerField(choices=[(0, 'Waiting for Payment'), (1, 'Preparing Order'), (2, 'Order is Prepared'), (3, 'Order in Shipping'), (4, 'Order is Delivered'), (5, 'Cancelled')], default=0, verbose_name='Order Status')),
                ('payment_option', models.CharField(choices=[('Cash On Delivery', 'Cash On Delivery'), ('Bkash', 'Bkash')], default='Cash On Delivery', max_length=20, verbose_name='Payment Options')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created in')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified in')),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store_app.customer')),
            ],
            options={
                'verbose_name': 'Order',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('price', models.FloatField()),
                ('discount_price', models.FloatField(default=0.0)),
                ('digital', models.BooleanField(blank=True, default=False, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='WishListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store_app.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store_app.product')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_discount', models.FloatField(default=0.0)),
                ('order_limit', models.IntegerField(default=50)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='store_app.product')),
            ],
        ),
        migrations.CreateModel(
            name='SoldItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_price', models.FloatField(default=0.0)),
                ('purchase_price', models.FloatField(default=0.0)),
                ('quantity', models.IntegerField(default=0)),
                ('discount', models.FloatField(default=0.0)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store_app.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store_app.product')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, null=True)),
                ('city', models.CharField(max_length=200, null=True)),
                ('state', models.CharField(max_length=200, null=True)),
                ('zipcode', models.CharField(max_length=200, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store_app.customer')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store_app.order')),
            ],
        ),
        migrations.CreateModel(
            name='PurchasedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_price', models.FloatField()),
                ('purchase_price', models.FloatField()),
                ('quantity', models.IntegerField(default=0)),
                ('product_source_name', models.CharField(max_length=200, null=True)),
                ('buying_time', models.DateTimeField(auto_now_add=True)),
                ('expiry_date', models.DateTimeField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store_app.product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store_app.order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store_app.product')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('is_checked', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store_app.cart')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store_app.product')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store_app.customer'),
        ),
    ]
