from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from customer_app.api import views as customer_views

urlpatterns = [
    path('register/', customer_views.register, name = "register"),
    path('login/', obtain_auth_token, name = "login"),
    path('logout/', customer_views.logout, name = "logout"),
    
    path('profile/', customer_views.profile, name = "profile"),
    path('wishlist/', customer_views.WishListAV.as_view(), name = 'wishlist'),
    path('order-list/', customer_views.OrderListAV.as_view(), name = 'order-list'),
    path('order-details/<int:pk>', customer_views.OrderDetailsAV.as_view(), name = 'order-details'),
]