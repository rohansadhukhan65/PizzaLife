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

import uuid

# Create your views here For Customer.
# home


def home(request):
    # print(request.META['HTTP_HOST'])
     
    return render(request, 'index.html')


# singup
def signup(request):

    if request.method == 'POST':
        SignForm = signUp(request.POST)
        if SignForm.is_valid():
             
            SignForm.save()

            print()

            
            user = User.objects.filter(username=SignForm.cleaned_data['username']).first()
            user.is_active = 0
            user.save()


            link = str(request.META['HTTP_HOST'])+'/loginCustomerverification/'+str(uuid.uuid4())

            subject = f'PizzaLife User Verification ! '
            message = f'Please Login From the Link Below and Veriify Your Email \n Link : {link}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [SignForm.cleaned_data['username']]
            send_mail( subject, message, email_from, recipient_list )
            
            return render(request, 'signup.html', {'Signform': SignForm,'msg':'Please Confirm Your Email by login with the email link'})
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



# login for active
def loginCustomerverify(request, ik):

    if request.method == 'POST':

        fmm = AuthenticationForm(request=request, data=request.POST)

        gt_user = User.objects.filter(username=request.POST.get('username', '')).first()
        gt_user.is_active = 1
        gt_user.save()
        if fmm.is_valid():
            uname = fmm.cleaned_data['username']
            upass = fmm.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                
                return HttpResponseRedirect('/UserHome')


    else:
        fmm = AuthenticationForm()
    return render(request, 'loginCustomer.html', {'fm': fmm})



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
    if request.user.is_authenticated:
        if request.method == "POST":
            print('we are in post')
            
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

            get_cart = Cart.objects.filter(user=request.user)

            i = 1
            Citem = ''
            for l in get_cart:

                Citem += f'{i}.{l.product.product_name} \n \n'
                i +=1


            order = Orders(items_json=Citem, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone_No=phone)
            order.save()
            thank = True
            id = order.order_ids

        
            # Emailing
            subject = f'{name.split()[0]}  Your Order Has Been Placed  !  '
            message = f'{name.split()[0]} Thank You For Order  !. We recived your order of \n {Citem} and we will contact you as soon as your order is shipped'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email ]
            send_mail( subject, message, email_from, recipient_list )

            
 
            # Gtotal = 0
            # for c in get_cart:
            #     Ptotal = int(c.product.price) * int(c.qty)
            #     Gtotal += int(Ptotal)

            
                
  
            return render(request, 'Checkout.html', {'thank': thank, 'id': id ,'name': request.user,'kart':get_cart,'gtotal':0,'po':1})
        # print('outer if')

        get_cart = Cart.objects.filter(user=request.user)

        Gtotal = 0
        if get_cart:
            for c in get_cart:
                Ptotal = int(c.product.price) * int(c.qty)
                Gtotal += int(Ptotal)


        return render(request, 'Checkout.html', {'thank': False, 'name': request.user,'kart':get_cart,'gtotal':Gtotal,'po':2})
    else:
        return HttpResponseRedirect('/loginCustomer')
    



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
def addcart(request):
    proId = request.POST['pid']
    custId = request.POST['cid']
 
    # print(proId)
    # print(custId)
    gt_user = User.objects.filter(id__icontains= custId ).first()
    # print(gt_user.username)
    gt_prod = Product.objects.filter(id__icontains= proId ).first()
    # print(gt_prod)
    # print()


    ifExist = Cart.objects.filter(Q(product=gt_prod) & Q(user=gt_user)).first()

    qantity = 0


    if ifExist:
        # print('exist',ifExist.qty)
        cart = Cart.objects.update_or_create(product=gt_prod, user=gt_user, defaults={'product': gt_prod, 'user': gt_user, 'qty': ifExist.qty + 1})
        qantity = ifExist.qty+1
       
    else:
        # print('not exist')
        cart = Cart.objects.update_or_create(product=gt_prod, user=gt_user, defaults={'nameprod':gt_prod.product_name,'product': gt_prod, 'user': gt_user, 'qty': 1})
        qantity =  1
 
    return JsonResponse({'Qtity':  qantity})





@csrf_exempt
def minuscart(request):
    proId = request.POST['pid']
    custId = request.POST['cid']
 
    # print(proId)
    # print(custId)
    gt_user = User.objects.filter(id__icontains= custId ).first()
    # print(gt_user.username)
    gt_prod = Product.objects.filter(id__icontains= proId ).first()
    # print(gt_prod)
    # print()

    
    ifExistm = Cart.objects.filter(Q(product=gt_prod) & Q(user=gt_user)).first()

   


    if ifExistm:
        # print('exist', ifExistm.qty) 'product': gt_prod, 'user': gt_user,
        if ifExistm.qty > 1 :
            cart = Cart.objects.update_or_create(product=gt_prod, user=gt_user, defaults={ 'qty': ifExistm.qty - 1})
            qantity = ifExistm.qty - 1
           

 
    return JsonResponse({'Qtity': qantity})






@csrf_exempt
def popover(request):
    UIddd = request.POST['uid']
    get_Uu = User.objects.filter(id = UIddd).first()

    cartItem = Cart.objects.filter(user=get_Uu).values()
    cartItemcount = Cart.objects.filter(user=get_Uu).count()

    Citem = list(cartItem)
    print()
    print()
    print()
    print('item :-',Citem)
    print(cartItemcount)
    print()
    print()
  
 
           

 
    return JsonResponse({'cart': Citem, 'count': cartItemcount})
    




@csrf_exempt
def clCart(request):
 
    UIdd = request.POST['uid']
    get_U = User.objects.filter(id = UIdd).first()
    gt_Cprodd = Cart.objects.filter(user=get_U)
 
    for k in gt_Cprodd:
        k.delete()
 

     

   
 
    return JsonResponse( {'hi':'hi'})


@csrf_exempt
def CartitemDel(request):
 
    Cid = request.POST['Cid']
    pid = request.POST['Pid']
    
    get_prod = Product.objects.filter(id = pid).first()
    get_Usr = User.objects.filter(id = Cid).first()
    gt_Cproddu = Cart.objects.filter(Q(user=get_Usr) & Q(product=get_prod)).first()

    gt_Cproddu.delete()
    
 
 
    return JsonResponse( {'hi':'hi'})