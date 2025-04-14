from django.shortcuts import redirect,render

from django.http import HttpResponse

from .forms import CreateUserForm, LoginForm

from payment.forms import ShippingForm

from payment.models import ShippingAddress

from django.contrib.sites.shortcuts import get_current_site

from .token import user_tokenizer_generate

from django.template.loader import render_to_string

from django.utils.encoding import force_bytes,force_str

from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

from django.contrib.auth.models import User

from django.contrib.auth.models import auth

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required





# Create your views here.

def register(request):

    form=CreateUserForm()

    if request.method == 'POST':

        form=CreateUserForm(request.POST)

        if form.is_valid():

            user= form.save()

            user.is_active=True

            user.save()

            #Email verification setup

            current_site=get_current_site(request)

            subject='Account verificaction email'

            message= render_to_string('account/registration/email-verification.html', {
                'user':user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),


            })

            user.email_user(subject=subject,message=message)





            return redirect('email-verification-sent')
        
    context={'form':form}   

    return render(request,'account/registration/register.html',context=context)


def email_verification(request,uidb64,token):

    unique_id=force_str(urlsafe_base64_decode(uidb64))

    user= User.objects.get(pk=unique_id)

    #success
    if user and user_tokenizer_generate.check_token(user,token):

        user.is_active=True

        user.save()

        return redirect('email-verification-success')

    #failed
    else:

        return redirect('email-verification-failed')



def email_verification_sent(request):

    return render(request,'account/registration/email-verification-sent.html')


def email_verification_success(request):

    return render(request,'account/registration/email-verification-success.html')




def email_verification_failed(request):

    return render(request,'account/registration/email-verification-failed.html')


def my_login(request):

    form=LoginForm
    if request.user.is_authenticated:#updated
        print("User already logged in, redirecting to dashboard...")
        return redirect('dashboard')

    if request.method=='POST':
        print("POST request received.")
        form=LoginForm(request,data=request.POST)
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        print(form.errors)
       
        print(user)

        if form.is_valid():
            
            username=request.POST.get('username')
            password=request.POST.get('password')

            user=authenticate(request,username=username,password=password)

            if user is not None:
                print("User {username} authenticated successfully.")
                auth.login(request,user)

                return redirect('dashboard')
            else:
                print("User {username} authentication failed")

        print("Form not valid")        

    context={'form':form}
    return render(request,'account/my-login.html',context=context)

#logout

def user_logout(request):

    auth.logout(request) 

    return redirect('store')


@login_required(login_url='my-login')
def dashboard(request):
    return render(request,'account/dashboard.html')


#Shipping view

def manage_shipping(request):
    
    try:
        #Account user with shipping information

        shipping=ShippingAddress.objects.get(user=request.user.id)
    
    except ShippingAddress.DoesNotExist:

        #Account user with no shipping information
        shipping=None
    
    form = ShippingForm(instance=shipping)

    if request.method=='POST':

        form=ShippingForm(request.POST,instance=shipping)

        if form.is_valid():
            #assign the user fk on the object
            shipping_user=form.save(commit=False)

            #Adding thr FK itself

            shipping_user.user=request.user

            shipping_user.save()

            return redirect('dashboard')
    
    context={'form':form}

    return render(request,'account/manage-shipping.html',context=context)

    



