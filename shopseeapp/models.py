from django.db import models
import datetime 
from django.utils import timezone
import os
from django.shortcuts import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# Create your models here.
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver




def getfilename(request,filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path.join('upload/',new_filename)


class Category(models.Model):
    categoryname=models.CharField(max_length=100)
    categoryimage=models.ImageField(upload_to=getfilename)
    status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    def __str__(self):
        return self.categoryname

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to=getfilename)
    status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True)
    productname = models.CharField(max_length=100)
    image=models.ImageField(upload_to=getfilename)
    status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    price = models.FloatField()
    quantity = models.IntegerField()
    discount_price = models.FloatField(blank=True, null=True)
    trending=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    offers=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    description = models.TextField()
    aboutproduct1 = models.TextField(blank=True, null=True)
    aboutproduct2 = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.productname

class Favourite(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    products=models.ForeignKey(Product,on_delete=models.CASCADE)
  



class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    products=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(null=True,blank=True,default=1)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
    @property
    def total_cost(self):
        return self.quantity*self.products.discount_price


    
  

    



class Contact(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    fname=models.CharField(max_length=20,null=True)
    lname=models.CharField(max_length=20,null=True)
    email=models.EmailField(max_length=100,null=True)
    comment=models.TextField(max_length=500,null=True)
    def __str__(self):
     return str(self.fname)
    

User=get_user_model()

def profilepic(request,filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path.join('upload/',new_filename)

# 9344091643 199









class Profile(models.Model):
  
    Gender_choices=(

        (1,'male'),
        (2,'female'),
        (3,'others')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default = 'This is the default, title change it in profile',max_length=500, blank=True)
    phone_number = models.CharField(max_length=12, blank=True)
    birth_date = models.DateField(default="2000-05-20",null=True, blank=True)
    address=models.TextField(max_length=250,blank=True,null=True,default="Add Address")
    city=models.CharField(max_length=250,blank=True,null=True ,default="Add Address")
    Landmark=models.CharField(max_length=250,blank=True,null=True,default="Add Address")
    pincode=models.IntegerField(max_length=8,blank=True)
    profile_image = models.ImageField(default='userprofile.png', upload_to='users/', null=True, blank=True)
    Gender=models.PositiveSmallIntegerField(choices=Gender_choices,null=True,blank=True)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)



class payment_choices:
    SUCCESS = "Success"
    FAILURE = "Failure"
    COD = "Cash On Delivery"

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    phonenumber=models.IntegerField()
    products=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(null=True,blank=True,default=1)
    ordernotes=models.CharField(max_length=200,null=True,blank=True)
    email=models.EmailField(max_length=100,null=True,blank=True)
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    pincode=models.CharField(max_length=200)
    orderid=models.CharField(unique=True,max_length=100,null=True,default=None)
    payment_status=models.CharField(
            ("payment_choices"),
            default=payment_choices.FAILURE,
            max_length=254,
            blank=False,
            null=False,
    )
    processing_status=models.CharField(max_length=100,null=True,default='Pending')
    razorpay_order_id=models.CharField(max_length=100,null=True)
    razorpay_payment_id=models.CharField(max_length=200,blank=True)
    razorpay_signature=models.CharField(max_length=200,blank=True)
    datetime_of_payment=models.DateTimeField(default=timezone.now)
    
    
    def save(self,*args,**kwargs):
        if self.orderid is None and self.datetime_of_payment and self.id:
            self.orderid=self.datetime_of_payment.strftime('PAY2ME%Y%m%dODR')+str(self.id)
        return super().save(*args,**kwargs)
    
    
    def __str__(self):
        return self.firstname
    



class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    products=models.ForeignKey(Product,on_delete=models.CASCADE)
    Desc= models.TextField(max_length=1000)
    rate= models.PositiveSmallIntegerField()
    email=models.EmailField(max_length=100,null=True)
    created=models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.user.username