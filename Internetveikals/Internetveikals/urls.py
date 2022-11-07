"""Internetveikals URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from majaslapa.views import *
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns
from majaslapa import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.sakums.as_view(),name='sakums'),
    path('account/', account, name='account'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('account/login/', loginpage, name='login'),
    path('register/', register, name='register'),
    path('category/<slug:post_slug>', category, name='category'),
    path('logout/', logoutUser, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('shopingcart/', cart, name='cart'),
    path('product/<str:slug_url>', product_info, name='product'),


    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),

    path('password/', PasswordsChangeView.as_view(template_name='majaslapa/change-password.html'), name='password'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='majaslapa/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='majaslapa/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='majaslapa/password_reser_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='majaslapa/password_reser_done.html'), name='password_reset'),

    path('i18n/',include('django.conf.urls.i18n')),


] + i18n_patterns(
    path('', views.sakums.as_view(), name='sakums'),
    path('shopingcart/', cart, name='cart'),
    path('account/', account, name='account'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('account/login/', loginpage, name='login'),
    path('register/', register, name='register'),
    path('category/<str:slug_url>', category, name='category'),
    path('logout/', logoutUser, name='logout'),
    path('accounts/', include('allauth.urls')),
    path('password/', PasswordsChangeView.as_view(template_name='majaslapa/change-password.html'), name='password'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
SOCIAL_AUTH_URL_NAMESPACE = 'social'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)