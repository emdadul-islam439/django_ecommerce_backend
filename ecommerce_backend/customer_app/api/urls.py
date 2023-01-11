from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from customer_app.api import views as customer_views

urlpatterns = [
    path('register/', customer_views.register, name = "register"),
    path('profile/', customer_views.profile, name = "profile"),
    path('wishlist/', customer_views.wishList, name = 'wishlist'),
    path('order-list/', customer_views.orderList, name = 'order-list'),
    path('order-details/<int:pk>', customer_views.OrderDetailView.as_view(), name = 'order-details'),
    path('login/', auth_views.LoginView.as_view(template_name = "customers/login.html"), name = "login"),
    path('logout/', auth_views.LogoutView.as_view(template_name = "customers/logout.html"), name = "logout"),
]