from django.contrib import admin
from django.urls import path, include
from Customer import views

 
 
app_name = 'Customer'


urlpatterns = [

    path('', views.home, name='home'),
    path('loginCustomer/', views.loginCustomer, name='Login'),
    path('loginCustomerverification/<uuid:ik>', views.loginCustomerverify, name='loginCustomerverify'),
    path('signup/', views.signup, name='signup'),
    path('feedback/', views.feedback, name='feedback'),
    path('UserHome/', views.userhome, name='userhome'),
    path('Tracker/', views.Tracker, name='Tracker'),
    path('Checkout/', views.Checkout, name='Checkout'),
    path('AboutUs/', views.AboutUs, name='AboutUs'),
    path('ContactUs/', views.ContactUs, name='ContactUs'),
    path('Logout/', views.LogOut, name='Logout'),
    path('fpwd/', views.fpwd, name='fpwd'),
    path('otpverify/', views.otpverify, name='otpverify'),
    path('pwdreset/', views.pwdreset, name='pwdreset'),



    ############ Admin part ##########################

    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('admin_Logout/', views.adminlogout, name='admin_Logout'),
    path('admin_add_product/', views.AddProduct, name='admin_add_product'),
    path('admin_show_orders/', views.ShowOrders, name='admin_show_orders'),


    # ajax=============

    path('addcart/', views.addcart, name='addcart'),
    path('minuscart/', views.minuscart, name='minuscart'),
    path('popover/', views.popover, name='popover'),
    path('clCart/', views.clCart, name='clCart'),
    path('CartitemDel/', views.CartitemDel, name='CartitemDel'),

    # orderstatus URL

    path('Confirmed_Ordr/', views.Confirmed_Ordr, name='Confirmed_Ordr'),
    path('Cooked_order/', views.Cooked_order, name='Cooked_order'),
    path('Delivered_ordr/', views.Delivered_ordr, name='Delivered_ordr'),
    path('Recived_ordr/', views.Recived_ordr, name='Recived_ordr'),
    path('Cancel_ordr/', views.Cancel_ordr, name='Cancel_ordr'),

    



    
]  


