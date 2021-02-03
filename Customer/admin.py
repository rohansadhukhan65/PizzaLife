from django.contrib import admin
from .models import *
# Register your models here.

 



class productAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'subcategory', 'price', 'desc', 'pub_date', 'image')



 
 


class order(admin.ModelAdmin):
    list_display = ('id','order_ids','items_json', 'name', 'email', 'phone_No', 'address',  'city', 'state', 'zip_code')
 
admin.site.register(Product, productAdmin)
admin.site.register(Orders, order)
admin.site.register(Cart)


