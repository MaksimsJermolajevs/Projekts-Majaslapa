from unicodedata import category
from django.views.generic.base import View
from email import message
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage
from django.views.generic.list import ListView
from django.db.models import Q
from django.template import RequestContext
from django.urls import reverse
from django.http import HttpResponse

from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from django_banklink.forms import PaymentRequest
from django_banklink.utils import verify_signature
from majaslapa.models import Transaction
from majaslapa.signals import transaction_succeeded
from majaslapa.signals import transaction_failed



class sakums(ListView):
    def get(self, request):
        search_query = request.GET.get('search', '')
        if search_query:
            kategorija = Category.objects.filter(Q(name__icontains=search_query))
        else:
            kategorija = Category.objects.all().filter(is_active=True)

        p = Paginator(kategorija, 10)
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)

        return render(request, 'majaslapa/home.html', {'category_list': page})


@login_required(login_url='login/')
def account(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if  p_form.is_valid():
            p_form.save()
            return redirect('account') # Redirect back to profile page

    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form
    }

    return render(request, 'majaslapa/account.html', context)


def about(request):
    return render(request, 'majaslapa/about.html')


def loginpage(request):
    if request.method == 'POST':
        list(messages.get_messages(request))
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
            list(messages.get_messages(request))
            messages.success(request, "Registration sucessful")
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('login')
        else:
            messages.info(request, form.errors)


    context = {'form': form}
    return render(request, 'majaslapa/register.html', context)

class PasswordsChangeView(PasswordChangeView):
    form_class = FormChangePassword
    success_url = reverse_lazy('account')



def category(request, slug_url):
    kategorija = Category.objects.get(slug=slug_url)
    Preces = Product.objects.all().filter(category = kategorija)

    return render(request, 'majaslapa/Product.html',{'product_list': Preces, "kategorija":kategorija})

def product_info(request, slug_url):
    Preces = Product.objects.get(slug=slug_url)
    return render(request, 'majaslapa/product_info.html',{'Preces': Preces})

def contact(request):
    return render(request, 'majaslapa/contact.html')


def logoutUser(request):
    logout(request)
    return redirect('login')




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


#Groza funkcija:
#Groza lapa
@login_required(login_url='/account/login/')
def cart(request):
    return render(request, 'majaslapa/cart.html')

#Groza pievienošana
@login_required(login_url='/account/login/')
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#Groza niņemšana
@login_required(login_url='/account/login/')
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart")

#Groza daudzuma palielināšana
@login_required(login_url='/account/login/')
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)

    cart.add(product=product)
    return redirect("cart")

#Groza daudzuma pamazināšana
@login_required(login_url='/account/login/')
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart")

#Groza Izstītīt visu frozu
@login_required(login_url='/account/login/')
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart")


@login_required(login_url='/account/login/')
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')



@csrf_exempt
def response(request):
    if request.method == 'POST':
        data = request.POST
    else:
        data = request.GET
    if 'VK_MAC' not in data:
        raise Http404("VK_MAC not in request")
    signature_valid = verify_signature(data, data['VK_MAC'])
    if not signature_valid:
        raise Http404("Invalid signature. ")
    transaction = get_object_or_404(Transaction, pk = data['VK_REF'])
    if data['VK_AUTO'] == 'Y':
        transaction.status = 'C'
        transaction.save()
        transaction_succeeded.send(Transaction, transaction = transaction)
        return HttResponse("request handled, swedbank")
    else:
        if data['VK_SERVICE'] == '1901':
            url = transaction.redirect_on_failure
            transaction.status = 'F'
            transaction.save()
            transaction_failed.send(Transaction, transaction = transaction)
        else:
            url = transaction.redirect_after_success
        return HttpResponseRedirect(url)

def request(request, description, message, amount, currency, redirect_to):
    if 'HTTP_HOST' not in request.META:
        raise Http404("HTTP/1.1 protocol only, specify Host header")
    protocol = 'https' if request.is_secure() else 'http'
    url = '%s://%s%s' % (protocol, request.META['HTTP_HOST'], reverse(response))
    context = RequestContext(request)
    user = None if request.user.is_anonymous() else request.user
    context['form'] = PaymentRequest(description = description,
                                     amount = amount,
                                     currency = currency,
                                     redirect_to = redirect_to,
                                     message = message,
                                     user = user)
    return render("django_banklink/request.html", context)