from django.contrib import admin
from django.urls import path

from store_app.api import views as store_views

urlpatterns = [
    path('no-of-cart-items/', store_views.NoOfCartItemsAV.as_view(), name='no-of-cart-items'),
    path('store/', store_views.StoreAV.as_view(), name='store'),
    path('cart-page/', store_views.CartPageAV.as_view(), name='cart-page'),
    path('create-cart-item/', store_views.CreateCartItemGV.as_view(), name='create-cart-item'),
    path('cart-item-details/<int:pk>', store_views.CartItemDetailsGV.as_view(), name='cart-item-details'),
    path('checkout-page/', store_views.CheckoutPageAV.as_view(), name='checkout-page'),
    path('create-shipping-address/', store_views.CreateShippingAddressGV.as_view(), name='create-shipping-address'),
    path('shipping-details/<int:pk>', store_views.ShippingDetailsGV.as_view(), name='shipping-details'),
    path('update-registered-user-cart/', store_views.updateRegisteredUserCart, name='update-registered-user-cart'),
    path('update-cookie-cart/', store_views.updateCookieCart, name='update-cookie-cart'),
    path('update-item/', store_views.updateItem, name='update-item'),
    path('process-order/', store_views.processOrder, name='process-order'),
    path('complete-payment/', store_views.completePayment, name='complete-payment'),
    path('update-wishlist/', store_views.updateWishList, name='update-wishlist'),
    path('product-details/<int:pk>', store_views.ProductDetailView.as_view(), name='producut-details'),
]   