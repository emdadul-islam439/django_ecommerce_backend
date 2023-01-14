from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

import datetime
import json
from statistics import quantiles

from store_app.utils import cartData, guestOrder, cookieCart, getWishListItems, getCartItemList, getStockInfoList, getProductListFromCartItems
from store_app.models import Cart, Product, CartItem, ShippingAddress, WishListItem, Order, OrderItem, Stock, PurchasedItem, SoldItem
from store_app.api.serializers import ProductSerializer, CartItemSerializer, StockSerializer, CartWithItemSerializer, ShippingAddressSerializer, OrderSummarySerializer, WishListItemSerializer
from background_task_app.models import EmailSendingTask
from background_task_app.enums import SetupStatus


# Create your views here.
class NoOfCartItemsAV(APIView):
    def get(self, request):
        try:
            cart_info = Cart.objects.filter(customer=request.user.customer).first()
            cart_item_list = cart_info.cartitem_set.all()
            total_quantity = 0
            
            for item in cart_item_list:
                total_quantity += item.quantity
            
            return Response({'no_of_cart_items': f'{total_quantity}'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'Error': 'data not found'}, status=status.HTTP_404_NOT_FOUND)


class StoreAV(APIView):
    def get(self, request):
        try:
            product_with_stock_and_cart_info_list = []
            product_list = Product.objects.all()
            cart = Cart.objects.filter(customer=request.user.customer).first()

            for product in product_list:
                stock_info = Stock.objects.filter(product=product).first()
                cart_item_info = CartItem.objects.filter(cart=cart, product=product).first()
                
                product_with_stock_and_cart_info_list.append({
                    'product_info': ProductSerializer(product).data, 
                    'stock_info': StockSerializer(stock_info).data, 
                    'cart_item_info': CartItemSerializer(cart_item_info).data
                })
            # REMEMBER: Respose(exact_dict_object_name, staus=...) gives pretty response
            # REMEMBER: Respose(f"exact_dict_object_name", status=...) convert the pretty JSON to STRING
            # REMEMBER: Respose(json.dumps(exact_dict_object_name), status=...) gives awkward string values 
            #           like "/"product_info/": /"..../"" (adding a slash before all inverted commas)
            return Response(product_with_stock_and_cart_info_list, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'data not found'}, status=status.HTTP_404_NOT_FOUND)
        

class CartPageAV(APIView):
    def get(self, request):
        try:
            cart = Cart.objects.filter(customer=request.user.customer).first()
            serializer = CartWithItemSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'data not found'}, status=status.HTTP_404_NOT_FOUND)


class CreateCartItemGV(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    
    def get_queryset(self):
        return CartItem.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(cart=self.request.user.customer.cart)

class CartItemDetailsGV(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    

class CheckoutPageAV(APIView):
    def get(self, request):
        try:
            shippingAddress_list = ShippingAddress.objects.filter(customer=request.user.customer)
            shipping_serializer = ShippingAddressSerializer(shippingAddress_list, many=True)
            
            cart = Cart.objects.filter(customer=request.user.customer).first()
            order_summary_serializer = OrderSummarySerializer(cart)
            
            checkout_page_info = {
                'shipping_address_list': shipping_serializer.data, 
                'order_summary': order_summary_serializer.data
            }
            return Response(checkout_page_info, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'data not found'}, status=status.HTTP_404_NOT_FOUND)


class CreateShippingAddressGV(generics.CreateAPIView):
    serializer_class = ShippingAddressSerializer
    
    def get_queryset(self):
        return ShippingAddress.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)
        

class ShippingDetailsGV(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ShippingAddressSerializer
    queryset = ShippingAddress.objects.all()


class CreateWishlistItemGV(generics.CreateAPIView):
    serializer_class = WishListItemSerializer
    
    def get_queryset(self):
        return WishListItem.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)
        

class WishlistItemDetailsGV(generics.RetrieveDestroyAPIView):
    serializer_class = WishListItemSerializer
    queryset = WishListItem.objects.all()
        

class ProductDetailsGV(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
        
    
def store(request):
    cookieData = cartData(request=request)
    products = Product.objects.all()
    cartItemList = getCartItemList(request, products, cookieData)
    stockInfoList = getStockInfoList(products)
    
    productInfoList = list(zip(products, cartItemList, stockInfoList))
    print(f"........STORE PAGE......  noOfCartItems = {cookieData['noOfCartItems']}  productInfoList={productInfoList}")
    context={'productInfoList' : productInfoList, 'noOfCartItems':  cookieData['noOfCartItems']}
    return render(request, 'store/store.html', context)


def cart(request):
    cookieData = cartData(request=request)
    items = cookieData['items']
    
    products = getProductListFromCartItems(request, items)
    stockInfoList = getStockInfoList(products)
    
    cartInfoList = list(zip(items, stockInfoList))
    context={'cartInfoList': cartInfoList, 'cart': cookieData['cart'], 'noOfCartItems':  cookieData['noOfCartItems']}
    
    if not request.user.is_authenticated:
        messages.success(request, "Guest Checkout Feature!! You can now order without Login into the site! If all the cart-items are digital, you will not have to give your shipping address also!")
    return render(request, 'store/cart.html', context)


def checkout(request):
    cookieData = cartData(request=request)
    items = cookieData['items']
    checked_item_count = 0
    is_all_item_available = True
    
    for item in items:
        if request.user.is_authenticated:
            if item.is_checked: checked_item_count += 1
            
            stockInfo = Stock.objects.filter(product=item.product).first()
            if stockInfo.effective_order_limit < item.quantity: 
                is_all_item_available = False
        else:
            if item['is_checked']: checked_item_count += 1
            
            product = Product.objects.get(id=item['product']['id'])
            stockInfo = Stock.objects.filter(product=product).first()
            if stockInfo.effective_order_limit < item['quantity']: 
                is_all_item_available = False
        
    if checked_item_count == 0 or not is_all_item_available:
        return redirect('/cart/')
    
    context={ 'items': items, 'cart': cookieData['cart'], 'noOfCartItems':  cookieData['noOfCartItems'] }
    if not request.user.is_authenticated:
        messages.success(request, "You can now order from us without Login into the site!")
    return render(request, 'store/checkout.html', context)


def updateRegisteredUserCart(request):
    print(f"updateRegisteredUserCart---> request.body={request.body}")
    data = json.loads(request.body)
    print(f"cartId = {data['cartId']} ")
    
    cart, created = Cart.objects.get_or_create(id=data['cartId'])
    cartItems = CartItem.objects.filter(cart=cart)
    
    for item in cartItems:
        stockInfo = Stock.objects.filter(product=item.product).first()
        if stockInfo.effective_order_limit == 0:
            item.is_checked = False
        else:
            item.quantity = min(stockInfo.effective_order_limit, item.quantity)
        item.save(update_fields=['is_checked', 'quantity'])
    return JsonResponse('OK', safe=False)


def processOrder(request):
    print('request.body: ', request.body)
    data = json.loads(request.body)
    print(f"data : {data}")
    
    transaction_id = datetime.datetime.now().timestamp()
    
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
    else:
        customer, cart = guestOrder(request=request, data=data)
        
    total = float(data['form']['total'])
    
    if total == cart.get_cart_total:
        now_time = datetime.datetime.now()
        print(f'now_time = {now_time}  type(now_time) = {type(now_time)}')
        
        order = Order.objects.create(
            customer=customer,
            transaction_id=transaction_id
        )
        EmailSendingTask.objects.create(
            order=order,
        )
        
        cartItems = CartItem.objects.filter(cart=cart, is_checked=True)
        for item in cartItems:
            OrderItem.objects.create(
                product=item.product,
                order=order,
                quantity=item.quantity,
            )
            item.delete()
    
    if cart.shipping == True:
        shipping_address = ShippingAddress.objects.create( 
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
        order.is_shipped = True
        order.shipping_address = shipping_address
        order.save(update_fields=['is_shipped', 'shipping_address'])
        
    return JsonResponse(f'{order.id}', safe=False)


def completePayment(request):
    print(f'in completePayment():  data = {request.body}')
    data = json.loads(request.body)
    print(f'data after json-decode = {data}')
    
    order, created = Order.objects.get_or_create(id=data['order_id'])
    
    if order.order_status == 5:
        return_message = 'Order is already cancelled!'
    else:
        order.order_status = 1
        order.save(update_fields=['order_status'])
        
        emailSendingTask = EmailSendingTask.objects.get(order=order)
        emailSendingTask.status = SetupStatus.disabled
        emailSendingTask.save(update_fields=['status'])
        
        return_message = 'success!'
        
    return JsonResponse(return_message, safe=False) 
    

def updateWishList(request):
    print('in updateWishList() --->  Data: ', request.body)
    data = json.loads(request.body)
    print(f"Data : {data}")
    response = ''
    
    if request.user.is_authenticated:
        customer = request.user.customer
        product = Product.objects.get(id=data['productId'])
        print(f"customer = {customer} | product_id = {data['productId']} | product.name = {product.name} ")
        wishListItem, created = WishListItem.objects.get_or_create(customer = customer, product = product)
        
        if data['action'] == 'add':
            wishListItem.save()
            response = 'Added to wish-list'
        elif data['action'] == 'remove':
            wishListItem.delete()
            response = 'Removed from wish-list'
    else:
        pass
    
    return JsonResponse(response, safe=False)


class ProductDetailView(DetailView):
    template_name: str = "store/product_details.html"
    context_object_name: str = "product"
    model = Product
    
    def get_context_data(self,*args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args,**kwargs)
        context['item'] = self.item
        context['noOfCartItems'] = self.noOfCartItems
        context['isInWishlist'] = self.is_in_wishlist
        return context
    
    def get(self, request, *args, **kwargs):
        self.cookieData = cartData(request=request)
        self.noOfCartItems = self.cookieData['noOfCartItems']
        self.items = self.cookieData['items']
        self.product_id = self.kwargs.get('pk')
        self.user_wishlist = [] if (request.user.is_anonymous) else WishListItem.objects.filter(product__id=self.product_id, customer=request.user.customer)
        self.is_in_wishlist = len(self.user_wishlist) > 0
        
        found_item = False
        for item in self.items:
            print(f'type(item) = {type(item)}  type(product_id) = {type(self.product_id)}')
            item_product_id = item.product.id if(request.user.is_authenticated) else item['product']['id']
            if item_product_id == self.product_id:
                self.item = item
                found_item = True
                break
        
        if not found_item:
            self.item = "NONE"
        print(f'product_id = {self.product_id}  item = {self.item},  noOfCartItems = {self.noOfCartItems},  user_wishlist = {self.user_wishlist}')
        return super(ProductDetailView, self).get(request, *args, **kwargs)
    
    
def stockItemList(request):
    cookieData = cartData(request=request)
    products = Stock.objects.all()
    print(f"........STORE PAGE......  noOfCartItems = {cookieData['noOfCartItems']}")
    
    context={ 'stockItemList' : products, 'noOfCartItems':  cookieData['noOfCartItems']}
    return render(request, "admin/store/stock/admin_stock_item_list.html", context)


def purchasedItemList(request):
    cookieData = cartData(request=request)
    products = PurchasedItem.objects.all()
    print(f"........STORE PAGE......  noOfCartItems = {cookieData['noOfCartItems']}")
    
    context={ 'purchasedItemsList' : products, 'noOfCartItems':  cookieData['noOfCartItems']}
    return render(request, "admin/store/purchaseditem/admin_purchased_item_list.html", context)


def soldItemList(request):
    cookieData = cartData(request=request)
    products = SoldItem.objects.all()
    print(f"........STORE PAGE......  noOfCartItems = {cookieData['noOfCartItems']}")
          
    context={ 'soldItemsList' : products, 'noOfCartItems':  cookieData['noOfCartItems']}
    return render(request, "admin/store/solditem/admin_sold_item_list.html", context)