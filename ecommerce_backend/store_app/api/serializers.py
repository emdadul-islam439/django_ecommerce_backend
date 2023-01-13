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
    class Meta:
        model = Order
        fields = '__all__'
    
    def get_order_item_list(self, object):
        allOrderItems = object.orderitem_set.all()
        serializer = OrderItemSerializer(allOrderItems, many=True)
        return serializer.data


class WishListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishListItem
        fields = '__all__'


class PurchasedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasedItem
        fields = '__all__' 


class SoldItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoldItem
        fields = '__all__' 


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'