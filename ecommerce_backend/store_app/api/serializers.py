import json
from rest_framework import serializers

from store_app.models import Product, Cart, CartItem, ShippingAddress, Order, OrderItem, WishListItem, PurchasedItem, SoldItem, Stock

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    cart_item_list = serializers.SerializerMethodField()
    customer = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Cart
        fields = '__all__'
        
    def get_cart_item_list(self, object):
        allCartItems = object.cartitem_set.all()
        serializer = CartItemSerializer(allCartItems, many=True)
        return serializer.data


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_item_list = serializers.SerializerMethodField()
    customer = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'
    
    def get_order_item_list(self, object):
        allOrderItems = object.orderitem_set.all()
        serializer = OrderItemSerializer(allOrderItems, many=True)
        return serializer.data


class StockSerializer(serializers.ModelSerializer):
    # product = serializers.StringRelatedField(read_only=True)
    product = serializers.SerializerMethodField()
    class Meta:
        model = Stock
        fields = '__all__'
    
    def get_product(self, object):
        print(f"vars(object) = {vars(object)}")
        # print(f"......vars(object.model) = {vars(object.model)}")
        product_info = Product.objects.filter(pk=object.product.id).first()
        serializer = ProductSerializer(product_info)
        return serializer.data


class WishListItemSerializer(serializers.ModelSerializer):
    stock_info = serializers.SerializerMethodField()
    cart_info = serializers.SerializerMethodField()
    class Meta:
        model = WishListItem
        fields = '__all__'

    def get_stock_info(self, object):
        stock_info = Stock.objects.filter(pk=object.product.pk).first()
        serializer = StockSerializer(stock_info)
        return serializer.data
    
    def get_cart_info(self, object):
        cart_info = CartItem.objects.filter(cart=object.customer.cart)
        serializer = CartItemSerializer(cart_info)
        return serializer.data
        
        
class PurchasedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasedItem
        fields = '__all__' 


class SoldItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoldItem
        fields = '__all__' 