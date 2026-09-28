from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_CUSTOMER = 'customer'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_CUSTOMER, 'Customer'),
    ]

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CUSTOMER)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.ROLE_ADMIN
        self.is_staff = self.is_superuser or self.role == self.ROLE_ADMIN
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username