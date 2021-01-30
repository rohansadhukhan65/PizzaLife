from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


#from Customer.models import user
from .models import *

 
#Feedback
class feeDBack(forms.Form):
    name = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control '}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control '}))
    feedback = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 20, 'class': 'form-control '}))
    

#SignUp
class signUp(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        labels = {'username':'Email'}
      


class ContactPizza(forms.Form):
    full_name = forms.CharField()
    Email = forms.EmailField()
    Messege = forms.CharField(widget = forms.Textarea(attrs={"rows":5,"cols":20}))
    
    
    



#OTP
class OTP(forms.Form):
    OTP = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control  '}))



############################################## admin part ######################################################

class Productsform(forms.Form):
    product_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control '}))
    category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control '}))
    subcategory = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control '}))
    price = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control '}))
    desc = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control '}))
    pub_date = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control '}))
    pub_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control '}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control '})) 
    

 

 
