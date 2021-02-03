from django.db import models
from django.contrib.auth.models import User
import random

# Create your  Databsae models here.

rando = random.randint(100000000000000 , 999999999999999)
randocart = random.randint(100000000000000 , 999999999999999)
############################################### Product Model ##########################################################
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    desc = models.CharField(max_length=300)
    pub_date = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/',null=True,blank=True)

    def __str__(self):
        return self.product_name
    
    

######################################################### Feedback Model ##################################################
""" class FeedBack(models.Model):
    name = models.CharField(max_length=70)
    email = models.EmailField(max_length=254)
    feedback = models.TextField()
 """
 
######################################################## Messege Us Model #####################################################
""" class Messegeus(models.Model):
    name = models.CharField(max_length=70)
    email = models.EmailField(max_length=254)
    messegee = models.TextField()
 """

######################################################## Order Model #####################################################
class Orders(models.Model):
    id = models.AutoField
    order_ids = models.CharField(   max_length=24, default=rando)
    items_json = models.CharField(max_length = 5000 ,default="")
    name = models.CharField(max_length=90, default="")
    email = models.EmailField(max_length=254 ,default=" ")
    phone_No = models.IntegerField(default=0)
    address = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    zip_code = models.CharField(max_length=50, default="")





######################################################## Cart Model #####################################################
class Cart(models.Model):
    id = models.AutoField
    cart_ids = models.CharField(max_length=24, default=randocart)
    nameprod = models.CharField(max_length=90, default="")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,   blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    qty = models.IntegerField(default=0)
    
 



    

 
