from django.urls import path
from api.views import get_all_products

urlpatterns = [
    path('all_products/', get_all_products),
]