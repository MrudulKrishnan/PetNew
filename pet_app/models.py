from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.

class User(AbstractUser):
    is_admin = models.BooleanField(default=False, verbose_name="Is admin")
    is_staff = models.BooleanField(default=False, verbose_name="Is Staff")
    is_customer = models.BooleanField(default=False, verbose_name="Is Customer")
    is_boy = models.BooleanField(default=False, verbose_name="Is Delivery Boy")
    name = models.CharField(max_length=100,null=True, blank=True)
    mobile = models.IntegerField(null=True, blank=True)
    Address = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=20,null=True, blank=True)
    role = models.CharField(max_length=20,null=True, blank=True)
    photo = models.ImageField(upload_to='profile/',null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.name

class Pet(models.Model):
    name = models.CharField(max_length=100,null=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='pet/',null=False)
    price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    description =models.CharField(max_length=300,null=False)
    breed=models.CharField(max_length=200,null=False)
    color=models.CharField(max_length=100,null=False)
    stock_level=models.IntegerField(null=False)
    age=models.CharField(max_length=100,null=False)
    vaccination = models.CharField(max_length=300,null=True)
    

class Products(models.Model):
    name =models.CharField(max_length=100,null=False)    
    category =models.ForeignKey(Category,on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='product/',null=False)
    price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True) 
    description = models.CharField(max_length=300,null=False)
    stock_level =models.IntegerField(null=False)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

    def total_price(self):
        return sum(item.total_price() for item in self.cart_items.all())

    def __str__(self):
        return f"Cart of {self.user.username}"

# CartItem Model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.content_object.price

    def __str__(self):
        return f"{self.quantity} x {self.content_object}"    
    
class BookingTable(models.Model):
    Date = models.DateField()
    Status = models.CharField(max_length=20)
    Total = models.FloatField()
    USER = models.ForeignKey(User, on_delete=models.CASCADE)


class BookingDetails(models.Model):
    Quantity = models.IntegerField()
    Status = models.CharField(max_length=30)
    PET = models.ForeignKey(Pet, on_delete=models.CASCADE)
    BOOK = models.ForeignKey(BookingTable, on_delete=models.CASCADE)

class AssignTable(models.Model):
    BOY = models.ForeignKey(User, on_delete=models.CASCADE)
    BOOKING = models.ForeignKey(BookingDetails, on_delete=models.CASCADE)
    Date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Status = models.CharField(max_length=30, blank=True, null=True)
      