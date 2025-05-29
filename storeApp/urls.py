from django.urls import path
from storeApp.views import index, add_to_cart, remove_from_cart, cart, add_review, delete_review, product_details, registro, login, toggle_wishlist, view_wishlist

urlpatterns = [
    path('', index, name = 'index'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name = 'add_to_cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name = 'remove_from_cart'),
    path('carrito/', cart, name = 'cart'),
    path('product/<int:product_id>/', product_details, name = 'product_details'),
    path('product/<int:product_id>/review/', add_review, name = 'add_review'),
    path('review/delete/<int:review_id>/', delete_review, name = 'delete_review'),
    path('registro/', registro, name = 'registro'),
    path('login/', login, name = 'login'),
    path('wishlist/toggle/<int:product_id>/', toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/', view_wishlist, name = 'view_wishlist'),
]