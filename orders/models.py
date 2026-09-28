from django.conf import settings
from django.db import models
from catalog.models import Product


class Order(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_SHIPPING = 'shipping'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Kutilmoqda'),
        (STATUS_SHIPPING, 'Yetkazilmoqda'),
        (STATUS_COMPLETED, 'Bajarildi'),
        (STATUS_CANCELLED, 'Bekor qilindi'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    shipping_address = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.id} - {self.user}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price_at_that_time = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'{self.product_name} x {self.quantity}'