from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import *
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from math import ceil

# Create your views here For Customer.
# home


def home(request):
    return render(request, 'index.html')


# singup
def signup(request):

    if request.method == 'POST':
        SignForm = signUp(request.POST)
        if SignForm.is_valid():
            print('posted')
            SignForm.save()
            return HttpResponseRedirect('/loginCustomer')
    else:
        SignForm = signUp()
        print('nehi gaya')

    return render(request, 'signup.html', {'Signform': SignForm})


# login
def loginCustomer(request):
    if request.method == 'POST':
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/UserHome')

    else:
        fm = AuthenticationForm()
    return render(request, 'loginCustomer.html', {'fm': fm})



# LogOut
def LogOut(request):
    logout(request)
    return HttpResponseRedirect('/')


# UserHome
def userhome(request):
    if request.user.is_authenticated:
        products = Product.objects.all()
        print(products)
        n = len(products)
        nSlides = n//4 + ceil((n/4)-(n//4))

        return render(request, 'UserHome.html', {'name': request.user, 'product': products, 'no_of_slides': nSlides, 'range': range(1, nSlides)})
    else:
        return HttpResponseRedirect('/loginCustomer')


#CheckOut
def Checkout(request):
    if request.method == "POST":
        print('we are in post')
        items_json = request.POST.get('itemsJson', '')
        print(items_json)
        name = request.POST.get('name', '')
        print(name)
        email = request.POST.get('email', '')
        print(email)
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        print(address)
        city = request.POST.get('city', '')
        print(city)
        state = request.POST.get('state', '')
        print(state)
        zip_code = request.POST.get('zip_code', '')
        print(zip_code)
        phone = request.POST.get('phone', '')
        print(phone)

        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone_No=phone)
        order.save()
        thank = True
        id = order.order_ids
        return render(request, 'Checkout.html', {'thank': thank, 'id': id ,'name': request.user,})
    print('outer if')
    return render(request, 'Checkout.html')
    



def Tracker(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        

    return render(request, 'Trcacker.html')



# AboutUs
def AboutUs(request):
    return render(request, 'AboutUs.html')


# Feedback
def feedback(request):
    if request.method == 'POST':
        feedbackform = feeDBack(request.POST)
        if feedbackform.is_valid():
            nm = feedbackform.cleaned_data['name']
            em = feedbackform.cleaned_data['email']
            fb = feedbackform.cleaned_data['feedback']
            save = FeedBack(name=nm, email=em, feedback=fb)
            save.save()
    else:
        feedbackform = feeDBack()

    return render(request, 'feedback.html', {'feedbForm': feedbackform})


# ContactUs
def ContactUs(request):
    if request.method == 'POST':
        cfm = ContactPizza(request.POST)
        if cfm.is_valid():
            nm = cfm.cleaned_data['full_name']
            em = cfm.cleaned_data['Email']
            msg = cfm.cleaned_data['Messege']
            save = Messegeus(name=nm, email=em, messegee=msg)
            save.save()
    else:
        cfm = ContactPizza()

    return render(request, 'ContactUs.html', {'fm': cfm})

##################################################### Admin Part ###############################################################

def adminlogin(request):
    if request.method == 'POST':
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/admin_home')

    else:
        fm = AuthenticationForm()
    return render(request, 'LoginAdmin.html', {'fm': fm})
   

def adminlogout(request):
    logout(request)
    return HttpResponseRedirect('adminlogin')


def admin_home(request):
    if request.user.is_authenticated:
        return render(request, 'admin_home.html')
    else:
        return HttpResponseRedirect('/adminlogin')


#----------------------------add Product---------------------
def AddProduct(request):
    if request.method == 'POST':
        print('post')
        product_frm = Productsform(request.POST, request.FILES)

        if product_frm.is_valid():
            print('is valid')
            nm = product_frm.cleaned_data['product_name']
            print(nm)
            catgry = product_frm.cleaned_data['category']
            subcatgry = product_frm.cleaned_data['subcategory']
            pric = product_frm.cleaned_data['price']
            dec = product_frm.cleaned_data['desc']
            pdate = product_frm.cleaned_data['pub_date']
            img = product_frm.cleaned_data['image']
            print(img)
            
             

            save = Product(product_name=nm, category=catgry, subcategory=subcatgry, price=pric, desc=dec, pub_date=pdate,image=img)
            save.save()

        else:
            print('not valid')
    else:
        print('nhi aya')
      
        product_frm = Productsform()

    return render(request, 'add-product.html', {'product_frm': product_frm})


#----------------------- Show Orders ----------------------------

def ShowOrders(request):
    Order = Orders.objects.all()
    print(Order)
    return render(request, 'show_orders.html' , {'orders' : Order})



 
