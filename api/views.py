from django.shortcuts import render
from storeApp.models import Product
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
def get_all_products(request):
    queryset = Product.objects.all()
    res = serializers.serialize('json', queryset)
    return JsonResponse(res, safe=False)