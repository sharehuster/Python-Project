from django.db import models
from django.contrib.auth.models import User # for Login
from django.contrib.auth.forms import UserCreationForm

# Create your models here.
# 1 bang du lieu -> 1 class

class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_categories', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    # slug để tìm kiếm kiểu : //dien-thoai

    def __str__(self):
        return self.name

#change forms register of django
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2'] # la cac truong co san cua django


# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False)
#     # null = true: se luu gia tri rong (empty) la NULL (thay vi false)
#     # blank = true:  truong duoc phep trống (blank) 

#     name = models.CharField(max_length=200, null=True)
#     email = models.CharField(max_length=200, null=True)

#     def __str__(self):
#         return self.name



class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='product')
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    detail = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name
    
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    # customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True) # pointer to class Customer
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True) # pointer to class Customer

    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total




class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True) # pointer to class Customer
    order =  models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True) # pointer to class Customer
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True) # pointer to class Customer
    order =  models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True) # pointer to class Customer
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    mobile = models.CharField(max_length=10, null=True)

    def __str__(self):
        return str(self.address)