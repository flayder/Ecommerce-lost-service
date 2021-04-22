from ecommerce.settings import MEDIA_ROOT, MEDIA_URL
from accounts.models import Profile
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . forms import  SignUpForm
from . models import Profile
from django.contrib.auth.models import User

# Create your views here.

def user_login(request):

    if request.method == 'POST' :

        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
        else:            
            return render(request,'accounts/login.html',{'error':True})
        return redirect('shop:homepage')

    return render(request,'accounts/login.html')


@login_required
def user_logout(request):

    logout(request)
    return redirect('shop:homepage')


def user_signup(request):

    if(request.method == 'POST'):

        signup_form = SignUpForm(request.POST)
          
        if signup_form.is_valid():

            username = signup_form.cleaned_data['username']
            password = signup_form.cleaned_data['password']
            email = signup_form.cleaned_data['email']
            firstname = signup_form.cleaned_data['firstname']
            lastname = signup_form.cleaned_data['lastname']
            
            queryname = User.objects.filter(username=username )
            querymail = User.objects.filter(email=email)

            if queryname or querymail:
                form = SignUpForm()
                username_exists = False
                email_exists = False
                if querymail:
                    email_exists = True
                if queryname:
                    username_exists = True

                context_dict={'username_exists':username_exists,'email_exists':email_exists,'form':form}
                return render(request,'accounts/signup.html',context_dict)

            user = User.objects.create_user(username,email,password)
            
            user.first_name = firstname
            user.last_name = lastname

            # user.set_password(password)
            profile = Profile.objects.create(user =user)
            profile.set(first_name = firstname,last_name = lastname)
            profile.save()
            user.save()
            
            login(request,user)

            return redirect('accounts:signup_success')

    else:
        form = SignUpForm()
        context = {'form':form}
        return render(request,'accounts/signup.html',context)

def signup_success(request):
    return render(request,'accounts/signup_success.html')

def profilepage(request):
    profile = get_object_or_404(Profile,user = request.user)
    context = {
        'user' : request.user,
        'profile' : profile,
    }
    return render(request,'accounts/profile.html',context)

