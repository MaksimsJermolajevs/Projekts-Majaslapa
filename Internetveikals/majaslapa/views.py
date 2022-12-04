from unicodedata import category
from django.views.generic.base import View
from email import message
from .forms import *
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .tokens import account_activation_token
from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, send_mail
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from cart.cart import Cart
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.views.generic.list import ListView
from django.db.models import Q
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.utils.translation import gettext as _




def search(request):

    search_query = request.GET.get('search', '')
    if search_query:
        Preces = Product.objects.filter(Q(title__icontains=search_query))
    else:
        Preces = Product.objects.all()

    return render(request, 'majaslapa/Product.html',{
        'product_list': Preces,})


class sakums(ListView):
    def get(self, request):
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
            return redirect('account') # Redirect back to profile pag

    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form
    }

    return render(request, 'majaslapa/account.html', context)


@login_required(login_url='login/')
def deleteuser(request):

    user = request.user
    user.delete()
    return redirect('sakums')

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
            messages.warning(request, _('Nav pareizs lietotājvārds vai parole'))

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
            messages.success(request, _("Reģistrācija veiksmīga"))
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('login')
        else:
            messages.info(request, form.errors)


    context = {'form': form}
    return render(request, 'majaslapa/register.html', context)

class PasswordsChangeView(PasswordChangeView):
    form_class = FormChangePassword
    success_url = reverse_lazy('account')


class category(ListView):
    def get(self, request, slug_url):

        price_from = request.GET.get('price_from', 0)
        price_to = request.GET.get('price_to', 1000)

        filtrs = request.GET.get('filter')

        kategorija = Category.objects.get(slug=slug_url)

        if filtrs:
            Preces = Product.objects.all().filter (Q(category = kategorija)).filter(regular_price__gte=price_from).filter(regular_price__lte=price_to).filter(productspecificationvalue__value__contains = filtrs)
        else:
            Preces = Product.objects.all().filter (Q(category = kategorija)).filter(regular_price__gte=price_from).filter(regular_price__lte=price_to)


        if Product.objects.all().filter (Q(category = kategorija)):
            obj  = Product.objects.all().filter (Q(category = kategorija)).first()
            Specifikacija = ProductSpecification.objects.all().filter(Q(Product_type__id__contains= obj.product_type.id))
            SpecifikacijaVertiba = ProductSpecificationValue.objects.all()
        else:
            Specifikacija = ''
            SpecifikacijaVertiba = ''

        if SpecifikacijaVertiba == SpecifikacijaVertiba:
            SpecifikacijaVertiba == ''



        p = Paginator(Preces, 10)
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
    # Specifikacijas_id = ProductSpecification.objects.values_list('id')
    # specifikacijas_vertiba = ProductSpecificationValue.objects.filter(specification_id__in = Specifikacijas_id)

        return render(request, 'majaslapa/Product.html',{
            'product_list': page,
            'kategorija':kategorija,
            'Specifikacija':Specifikacija,
            'Specifikacija_veriba':SpecifikacijaVertiba,
            'price_from':price_from,
            'price_to':price_to,
        })


def product_info(request, slug_url):
    logged_user = request.user
    user_id = logged_user.id
    # stripe_webhook(user_id)
    Preces = Product.objects.get(slug=slug_url)
    return render(request, 'majaslapa/product_info.html',{'Preces': Preces})

def contact(request):
    if request.method == 'POST':
        contact = Contact()
        name = request.POST.get('name')
        email = request.POST.get('e-mail')
        subject = request.POST.get('subject')
        details = request.POST.get('details')

        contact.name = name
        contact.email = email
        contact.subject = subject
        contact.details = details
        contact.save()

        messages.success(request, _("Jūsu vēstule tika nosūtia mums!"), extra_tags='alert')
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
        messages.error(request, _('Aktivizācijas saite nav derīga!'))
    return redirect('login')


def activateEmail(request, user, to_email):
    # username = user.username
    mail_subject = 'Aktivizējiēt savu konu Baltictech'
    Email = [to_email]

    context = {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": "https" if request.is_secure() else 'http'
    }
    message = render_to_string('majaslapa/template_activate_account.html', context=context)

    email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER ,to=Email)
    email.content_subtype = 'html'
    email.fail_silently = False

    # email.content_subtype = 'html'
    if email.send():
        messages.success(request, _(f'Cien {user}, lūdzu dodieties uz e-pasta {Email} iesūtni un noklikšķiniet uz \
            saņemta aktivizācijas saite, lai apstiprinātu un pabeigtu reģistrāciju. Piezīme: Ja neredzat vēstūli, lūdzu pārbaudiet mēstules mapi.'))
    else:
        messages.error(request, _(f'Notika problēma, sūtot e-pastu uz {Email}, pārbaudiet, vai ierakstījāt pareizi.'))
# Create your views here.

import uuid
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
@login_required(login_url='/account/login/')
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@login_required(login_url='/account/login/')
@csrf_exempt
def create_checkout_sessionn(request, slug_url):
    user = request.user
    Preces = Product.objects.get(slug=slug_url)
    if Preces.discount_price is None:
        Price = Preces.regular_price
    else:
        Price = Preces.discount_price
    if request.method == 'GET':
        domain_url = 'http://127.0.0.1:8000/'+Preces.slug
        doamin = 'http://127.0.0.1:8000'
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            checkout_session = stripe.checkout.Session.create(
                success_url = domain_url + '/success/',#?session_id={CHECKOUT_SESSION_ID}
                cancel_url = domain_url + '/cancelled/',
                payment_method_types=['card'],
                line_items = [
                    {
                        'quantity': 1,
                        'price_data' : {
                            'currency': "eur",
                            'unit_amount' : int(Price * 100),
                        'product_data': {
                            'name': Preces.title,
                            'description': Preces.desciption,
      },
                }
                    }
                ],
                metadata= {
                    'product_id' : Preces.id,
                    'client_reference_id' : user.id},
                mode='payment',
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

from django.views.generic import TemplateView
class SuccessView(TemplateView):
    template_name = 'majaslapa/test1.html'


class CancelledView(TemplateView):
    template_name = 'majaslapa/test2.html'


@csrf_exempt
def stripe_webhook(request):
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session['customer_details']['email']
        product_id = session['metadata']['product_id']
        user_id = session['metadata']['client_reference_id']
        Order_number = session['created']
        amount = session['amount_total']
        product = Product.objects.get(id=product_id)

        send_mail(
            subject='Paldies ka iegadajaties produktu no mūsu veikala',
            message='Paldies, par pirkumu',
            recipient_list=[customer_email],
            from_email='balticctech@gmail.com',
        )

        orders.objects.create(
            Order_number=Order_number,
            quantity= 1,
            amount = amount / 100,
            product_id = product_id,
            user_id = user_id
         )

    return HttpResponse(status=200)

@login_required(login_url='/account/login/')
@csrf_exempt
def create_checkout_session(request, slug_url):
    user = request.user
    Preces = Product.objects.get(slug=slug_url)
    if Preces.discount_price is None:
        Price = Preces.regular_price
    else:
        Price = Preces.discount_price
    if request.method == 'GET':
        domain_url = 'http://127.0.0.1:8000/'+Preces.slug
        doamin = 'http://127.0.0.1:8000'
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            checkout_session = stripe.checkout.Session.create(
                success_url = domain_url + '/success/',#?session_id={CHECKOUT_SESSION_ID}
                cancel_url = domain_url + '/cancelled/',
                payment_method_types=['card'],
                line_items = [
                    {
                        'quantity': 1,
                        'price_data' : {
                            'currency': "eur",
                            'unit_amount' : int(Price * 100),
                        'product_data': {
                            'name': Preces.title,
                            'description': Preces.desciption,
      },
                }
                    }
                ],
                metadata= {
                    'product_id' : Preces.id,
                    'client_reference_id' : user.id},
                mode='payment',
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
