from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_description = models.CharField(max_length=250)
    product_full_cost = models.DecimalField(max_digits=8, decimal_places=2, default=999.00)
    product_offer_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    imagen = models.CharField(max_length=100, default='default.jpg')
    
    @property
    def imagen_url(Self):
        return f'storeApp/img/{Self.imagen}'

    def __str__(Self):
        return Self.product_name
    
    def has_offer(Self):
        return Self.product_offer_cost is not None and Self.product_offer_cost < Self.product_full_cost

    def format_price_mxn(Self, price):
        return f"${price:,.2f} MXN"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.TextField(max_length=500)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    date = models.DateTimeField(default = timezone.now)

    def local_date(Self):
        return timezone.localtime(Self.date)

    def __str__(Self):
        return f"Reseña de {Self.product.product_name} por {Self.username}"
