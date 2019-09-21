from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
from rest_framework.views import APIView
from .forms import UserRegisterationForm,UserLoginForm
import logging
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils import timezone
from .models import User


class ApiRegistration(APIView):
    def get(self, request):
        form = UserRegisterationForm()
        return render(request, "login_register/register.html",{'form':form})

    def post(self, request):
        logger = logging.getLogger('request')
        logger.error(request.data)
        print(request.POST)
        userRegisterForm = UserRegisterationForm(request.POST)
        if userRegisterForm.is_valid():
           email=userRegisterForm.cleaned_data['email']
           try :
             user=User.objects.get(email=email)
             user.first_name=userRegisterForm.cleaned_data['first_name']
             user.set_password(userRegisterForm.cleaned_data['password'])
             user.save()
           except:
               user = userRegisterForm.save()
               user.set_password(userRegisterForm.cleaned_data['password'])
               user.save()
           try:

                    current_site = get_current_site(request)
                    mail_subject = 'Varify your Account- IG Acceptor.'
                    message = render_to_string('acc_active_email.html', {
                        'user': user.email,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
                    to_email = userRegisterForm.cleaned_data.get('email')
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    if email.send():
                        messages.success(request,
                                         'We Sent a Verification mail to Your Email Id Please Verify your Email and Login !')
                        return redirect("login")

                    else:
                        print("form not valid")
                        messages.error(request, 'Please check you email ')
                        m = "Email Id given is Not valid !"

                        return redirect("register")
           except Exception as e:
                    print("outer try")
                    messages.error(request, 'Please check you email ')
                    print(e)
                    return redirect("register")
        else:
            print("form invalid")


class ApiLogin(APIView):
    def get(self,request):
        form =UserLoginForm()
        return render(request, 'login_register/login.html',{'form':form})

    def post(self, request):
        data = request.data
        email = data.get("email")
        password = data.get('password')

        try:
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.verified==True:
                    login(request, user)
                    messages.success(request,"Login Success !")
                    return redirect("dashboard")
                else:
                    messages.success(request,"We have sent you a Verification Mail Please Verify Your Email and Try to Login  !")
                    return redirect("login")
            else:
                messages.error(request, "Invalid Email or Password!")
                print("in else condtion")
                return redirect("login")


        except  Exception as e:
            messages.error(request, "Invalid Email or Password!")
            print("in except",e)
            return redirect("login")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(id=uid)
        print(user.email)
        print("user unabelgsgtjseog")
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    print("user token verirfy",account_activation_token.check_token(user, token))
    if user is not None and account_activation_token.check_token(user, token):
        user.verified =True
        user.save()
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')



