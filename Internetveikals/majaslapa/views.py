from django.views.generic.base import View
from email import message
from django.shortcuts import render, redirect
from .forms import  CreateUserForm
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .models import *

# from majaslapa.register_login.utils import send_email_for_verify

from django.contrib.auth import get_user_model



def activate(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request,"Paldies par e-pasta apstiprinājumu. Tagad varat pierakstīties savā kontā.")
        return redirect('login')
    else:
        messages.error(request,'Aktivizācijas saite nav derīga!')
    return redirect('login')

def activateEmail(request, user, to_email):
    mail_subject = 'Aktivizējiēt savu konu Baltictech.store'
    message = render_to_string('majaslapa/template_activate_account.html',{
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": "https" if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Cien {user}, lūdzu dodieties uz e-pasta {to_email} iesūtni un noklikšķiniet uz \
            saņemta aktivizācijas saite, lai apstiprinātu un pabeigtu reģistrāciju. Piezīme: Ja neredzat vēstūli, lūdzu pārbaudiet mēstules mapi.')
    else:
        messages.error(request, f'Notika problēma, sūtot e-pastu uz {to_email}, pārbaudiet, vai ierakstījāt pareizi.')
# Create your views here.

class sakums(View):
    def get(self, request):
        kategorija = Category.objects.all()
        return render(request, 'majaslapa/home.html', {'category_list': kategorija})

def account(request):
    return render(request, 'majaslapa/account.html')

def about(request):
    return render(request, 'majaslapa/about.html')



def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('sakums')
        else:
            messages.info(request, 'Nav pareizs lietotājvārds vai parole')

    context = {}
    return render(request, 'majaslapa/login.html', context)

def register(request):
    form = CreateUserForm(request.POST)

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('login')


    context = {'form': form}
    return render(request, 'majaslapa/register.html', context)

def search(request):
    return render(request, 'majaslapa/search.html')

def contact(request):
    return render(request, 'majaslapa/contact.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

