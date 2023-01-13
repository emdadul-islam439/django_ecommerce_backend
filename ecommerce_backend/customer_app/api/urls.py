from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from customer_app.api import views as customer_views

urlpatterns = [
    path('register/', customer_views.register, name = "register"),
    path('login/', obtain_auth_token, name = "login"),
    path('logout/', customer_views.logout, name = "logout"),
    
    path('profile/', customer_views.ProfileAV.as_view(), name = "profile"),
    path('wishlist/', customer_views.WishListGV.as_view(), name = 'wishlist'),
    path('order-list/', customer_views.OrderListGV.as_view(), name = 'order-list'),
    path('order-details/<int:pk>', customer_views.OrderDetailsGV.as_view(), name = 'order-details'),
]