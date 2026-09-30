from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
class Cards(models.Model):
    CARD_TYPE_CHOICES = [
        ("CREDIT","credit"),
        ("DEBIT","debit"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=15, choices=CARD_TYPE_CHOICES)
    card_number = models.CharField(max_length=16)
    last_four_digit = models.CharField(max_length=4)
    expiry_data = models.CharField(max_length=5)
    card_holder_name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10,decimal_places=2, default=Decimal("5000.00"))
class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
class AdminLogs(models.Model):
    admin = models.ForeignKey(
        User,on_delete=models.CASCADE
    )
    action = models. CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.admin.username} - {self.action}"

class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blacklisted token - {self.id}"
