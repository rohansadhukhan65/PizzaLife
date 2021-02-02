from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import *
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from math import ceil



# Email configuration
from django.conf import settings
from django.core.mail import send_mail
# Email configuration end


from django.contrib.auth.models import User
import random
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

       

        subject = f'{name.split()[0]}  Your Order Has Been Placed  !  '
        message = f'{name.split()[0]} Thank You For Order  !. We recived your order of \n {items_json} and will contact you as soon as your order is shipped'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email ]
        send_mail( subject, message, email_from, recipient_list )
        return render(request, 'Checkout.html', {'thank': thank, 'id': id ,'name': request.user,})
    print('outer if')
    return render(request, 'Checkout.html', {'thank': False,'name': request.user,})
    



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





# ===========================================  forget password system ======================================
def fpwd(request):
    
    Uemail = request.POST.get('forgetpwdemail', '')
    # print()
    # print()
    # print('========',Uemail)
    # print()
    # print()
    # print()
    if Uemail:
        getuser = User.objects.filter(username__icontains=Uemail).first()
    else:
        getuser = 0
    if getuser:
        

        # Getting OTP and id
        request.session['OTP'] = random.randint(000000,999999)
        request.session['Uid'] = getuser.id
        request.session.set_expiry(0)
        otp = request.session['OTP'] 
        

        # Sending OTP in Email
        subject = f'PizzaLife Password Reset OTP '
        message = f'{getuser.first_name} Your OTP is \n\n {otp}  '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [Uemail ]
        send_mail(subject, message, email_from, recipient_list)
        
        return HttpResponseRedirect('/otpverify/')
    print()
    print()
    print()
    print()


    return render(request, 'forgetpwd.html' )




def otpverify(request):
    Uotp = request.POST.get('otp', '')
    print()
    print()
    print()
    print()
    print('User OTP ==', Uotp)
    print('OTP==', request.session['OTP'])
    print('OTP==', request.session['Uid'])
    if Uotp == str(request.session['OTP']): 
        print("Matched !")
        request.session['OTP'] = ''
        eru=''
        return HttpResponseRedirect('/pwdreset/')
    else:
        eru = 'OTP Not Matched !'
    print()
    print()
    print()

    return render(request, 'otppage.html',{'errmsg':''})




def pwdreset(request):
    print()
    print()
    print()
    print()
    print(request.POST.get('newPwd', ''))

    newPwd = request.POST.get('newPwd', '')

    if newPwd:
        user = User.objects.get(id__icontains=request.session['Uid'])
    else:
        user = 0
        
    if user:
        print(user.password)
        user.set_password(newPwd)
         
        user.save()
        request.session['Uid'] = ''

        return HttpResponseRedirect('/loginCustomer/')

    print('Uid==', request.session['Uid'])
    print()
    print()
    print()
    print()

    return render(request, 'resetPwd.html' )
    







# =============  Ajax

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Subquery , Q


@csrf_exempt
def cart(request):
    proId = request.POST['pid']
    custId = request.POST['cid']
    print()
    print()
    print()
    print()
    print()
    print()
    print(proId)
    print(custId)
    gt_user = User.objects.filter(id__icontains= custId ).first()
    print(gt_user.username)
    gt_prod = Product.objets.filter(id__icontains= proId ).first()
    print(gt_prod)
    print()
    ifExist = Cart.objects.filter(Q(product=gt_prod) & Q(user=gt_user)).first()
    
    if ifExist:
        cart = Cart.objects.update_or_create(product=gt_prod, user=gt_user, defaults={'product': gt_prod, 'user': gt_user, 'qty': 1})
    else:
        cart = Cart.objects.update_or_create(product=gt_prod, user=gt_user, defaults={'product': gt_prod, 'user': gt_user, 'qty': 1})

    print()
    print()
    print()
    print()
    print()
    print()
    print()
    return JsonResponse({'cartdata': 'baner'})