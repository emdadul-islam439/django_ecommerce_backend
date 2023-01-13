from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, generics

from .serializers import RegistrationSerializer, CustomerSerializer
from customer_app.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from store_app.utils import cartData, getWishListItems, getTrackInfoList, getCartItemList, getStockInfoList
from store_app.models import Order, OrderItem, WishListItem
from store_app.api.serializers import OrderSerializer, WishListItemSerializer
from customer_app.models import AdminUser, Customer

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
    

class ProfileAV(APIView):
    # TODO: couldn't find a way to implement generics.RetrieveAPIView
    # TODO: if a generic view would be implemented, there would be less code and also less errors
    # serializer_class = CustomerSerializer
    # queryset = Customer.objects.filter(user=self.request.user).first()
    # def get_queryset(self):
    #     return Customer.objects.filter(user=self.request.user).first()
    
    def get(self, request):
        try:
            customer_info = Customer.objects.filter(user=request.user).first()
            serializer = CustomerSerializer(customer_info) # add "context={'request': request}" into the argument-list for HyperlinkedRelatedField
            print(f"serializer.data = {serializer.data}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        customer_info = Customer.objects.filter(user=request.user).first()
        serializer = CustomerSerializer(customer_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class WishListGV(generics.ListAPIView):
    serializer_class = WishListItemSerializer
    
    def get_queryset(self):
        return WishListItem.objects.filter(customer=self.request.user.customer)
    
    
class OrderListGV(generics.ListAPIView):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.customer)
    

class OrderDetailsGV(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Order.objects.filter(pk=pk)