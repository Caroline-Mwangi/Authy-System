from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from authSys import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import  urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token

def home(request):
    return render(request, "authentication/index.html")

def register(request):
    if request.method == "POST":
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        username = request.POST['uname']
        email = request.POST['email']
        password = request.POST['pass']
        c_pass = request.POST['cpass']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exists! Please try another one.")
            return redirect('register')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email is already registered!")
            return redirect('register')
        
        if len(username)>10:
            messages.error(request, "Username must be under 10 characters.")
            return redirect('register')
            
        if password != c_pass:
            messages.error(request, "Passwords don't match!")
            return redirect('register')
            
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('register')
        
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.is_active = False
        myuser.save()
        
        messages.success(request, "Yaayy! Your Details Have Been Successfully Submitted. Check your email for verification before you login.")
        
        #Welcome Email
        subject = "Welcome To Authy"
        message = "Hello, " + myuser.first_name + "!! \n" + "Thank you for choosing Authy!! \n We have sent you a confirmation email, kindly verify youur email address so as to activate your account. \n\n Kind Regards, \n Authy Team."
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Confirmation Email
        
        current_site = get_current_site(request)
        email_subject = "Confirm Your Authy Email"
        email_message = render_to_string('email_confirm.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email  = EmailMessage(
            email_subject,
            email_message,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('login')
    
    return render(request, "authentication/register.html")

def log_in(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['pass']
        
        #Authenticate user
        user = authenticate(username=username, password=password) 
        
        if user is not None:
            login(request, user)
            first_name = user.first_name
            return render(request, "authentication/landing.html", {'first_name' : first_name} )
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
        
    return render(request, "authentication/login.html")

def log_out(request):
    logout(request)
    messages.success(request, "Logged out successfully :)")
    return redirect('home')

def landing(request):
    return render(request, "authentication/landing.html")

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
        
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        return redirect('login')
    else:
        messages.error(request, "Activation Failed. Try Again!")
        return redirect('home')
    