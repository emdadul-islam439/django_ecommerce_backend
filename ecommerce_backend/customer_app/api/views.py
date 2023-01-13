from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, generics

from .serializers import RegistrationSerializer
from customer_app.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from store_app.utils import cartData, getWishListItems, getTrackInfoList, getCartItemList, getStockInfoList
from store_app.models import Order, OrderItem
from store_app.api.serializers import OrderSerializer
from customer_app.models import AdminUser

# Create your views here.
@api_view(['POST',])
def register(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            token = Token.objects.get(user=account).key
            status_code = status.HTTP_201_CREATED
            
            data['Response'] = "User created successfully!"
            data['username'] = account.username
            data['email'] = account.email
            data['token'] = token
        else:
            data = serializer.errors
            status_code = status.HTTP_400_BAD_REQUEST
        
        return Response(data, status=status_code)
    

@api_view(['POST'])
def logout(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    
    
class OrderListAV(generics.ListAPIView):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.customer)
    

class OrderDetailsAV(generics.ListAPIView):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Order.objects.filter(pk=pk)
    

def redirectUser(request):
    print('IN RE-DIRECT-USER')
    admin_users = AdminUser.objects.all()
    print(f'admin_users = {admin_users}')
    
    for admin in admin_users:
        print(f'admin.id = {admin.id} request.user.id = ', request.user.id)
        if request.user.id == admin.id:
            return redirect('admin/store/stock/', permanent=True)
    return redirect('store/', parmanent=True)


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, 
                                instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, 
                                   instance=request.user.customer)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated successfully!")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.customer)
    
    cookieData = cartData(request=request)
    noOfCartItems = cookieData['noOfCartItems']
    context = {
        "u_form" : u_form,
        "p_form" : p_form,
        "noOfCartItems" : noOfCartItems
    }
    return render(request, "customers/profile.html", context)
     
    
def wishList(request):
    cookieData = cartData(request=request)
    products = getWishListItems(request)
    cartItemList = getCartItemList(request, products, cookieData)
    stockInfoList = getStockInfoList(products)
    productInfoList = list(zip(products, cartItemList, stockInfoList))
    
    context = { 'productInfoList' : productInfoList, 'noOfCartItems':  cookieData['noOfCartItems']}
    return render(request, 'customers/wishlist.html', context)
    

@login_required 
def orderList(request):
    cookieData = cartData(request=request)
    orders = Order.objects.order_by('-id').filter(customer = request.user.customer)
    print('in orderList()------> ORDERS: ', orders)
    
    context={ 'orders' : orders, 'noOfCartItems':  cookieData['noOfCartItems']}
    return render(request, 'customers/order-list.html', context)


class OrderDetailView(DetailView):
    login_required = True
    template_name: str = "customer_app/order-details.html"
    context_object_name: str = "order"
    model = Order
    
    def get_context_data(self,*args, **kwargs):
        context = super(OrderDetailView, self).get_context_data(*args,**kwargs)
        context['items'] = self.items
        context['noOfCartItems'] = self.noOfCartItems
        context['trackInfoList'] = self.trackInfoList
        return context
    
    def get(self, request, *args, **kwargs):
        self.cookieData = cartData(request=request)
        self.noOfCartItems = self.cookieData['noOfCartItems']
        self.order_id = self.kwargs.get('pk')
        self.items = OrderItem.objects.filter(order__id=self.order_id)
        
        order = Order.objects.filter(id=self.order_id).first()
    
        if order.order_status == 5:
            return redirect('/order-list/')
        else:
            self.trackInfoList = getTrackInfoList(order.order_status)
            print(f'order_id = {self.order_id}  items = {self.items},  noOfCartItems = {self.noOfCartItems}')
            return super(OrderDetailView, self).get(request, *args, **kwargs)   
