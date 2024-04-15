from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,UserManager
from django.db import models
import uuid
from django.utils import timezone
# from order.models import MenuItem

class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    print(id,"id---------------")
    street = models.CharField(max_length=100,blank=True, null=True)
    city = models.CharField(max_length=100,blank=True, null=True)
    state = models.CharField(max_length=100,blank=True, null=True)
    country = models.CharField(max_length=100,blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,default='1243324')
    longitude = models.DecimalField(max_digits=9, decimal_places=6,default='345345')
    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}"

class CustomUserManager(UserManager):
    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)
    
    
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('driver', 'Delivery Driver'),
        ('restaurant', 'Restaurant Owner'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    # avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []


   

    def __str__(self):
        return self.email




class Customer(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    contact = models.CharField(max_length=15)
    favorite_restaurants = models.ManyToManyField('Restaurant', blank=True)

    def __str__(self):
        return self.user.name

class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True, related_name='rest_address')
    operating_hours = models.CharField(max_length=100)
    flat=models.FloatField(default=0)
    rating=models.FloatField(default=0)
    menu = models.ForeignKey('order.MenuItem', on_delete=models.CASCADE, null=True, blank=True, related_name='rest_address')

    def __str__(self):
        return self.name

class DeliveryPartner(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='delivery_man')
    contact_number = models.CharField(max_length=15)
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)
    bike_info = models.CharField(max_length=100, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def __str__(self):
        return self.user.name