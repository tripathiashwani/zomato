from django.db import models
from account.models import User,Customer,Restaurant,DeliveryPartner 
from django.db.models import Q


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category_choices = [
        ('appetizers', 'Appetizers'),
        ('main_course', 'Main Course'),
        ('desserts', 'Desserts'),
    ]
    category = models.CharField(max_length=20, choices=category_choices)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    restauarant=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} ({self.user.username})"