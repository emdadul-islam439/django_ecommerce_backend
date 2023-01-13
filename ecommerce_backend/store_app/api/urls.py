from django.contrib import admin
from django.urls import path

from store_app.api import views as store_views

urlpatterns = [
    path('no-of-cart-items/', store_views.NoOfCartItemsAV.as_view(), name = 'no-of-cart-items'),
    path('store/', store_views.StoreAV.as_view(), name = 'store'),
    path('cart-page/', store_views.CartPageAV.as_view(), name = 'cart-page'),
    path('checkout/', store_views.checkout, name = 'checkout'),
    path('update-registered-user-cart/', store_views.updateRegisteredUserCart, name = 'update-registered-user-cart'),
    path('update-cookie-cart/', store_views.updateCookieCart, name = 'update-cookie-cart'),
    path('update-item/', store_views.updateItem, name = 'update-item'),
    path('process-order/', store_views.processOrder, name = 'process-order'),
    path('complete-payment/', store_views.completePayment, name = 'complete-payment'),
    path('update-wishlist/', store_views.updateWishList, name = 'update-wishlist'),
    path('product-details/<int:pk>', store_views.ProductDetailView.as_view(), name = 'producut-details'),
]   