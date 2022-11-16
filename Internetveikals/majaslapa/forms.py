from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile
# from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe
from django.urls import reverse


User = get_user_model()

class CreateUserForm(UserCreationForm):

    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'required': 'True',
            'verbose_name':'Lietotāvārds'
        }),
    )


    password1 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'required': 'True'
        }),
    )

    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'required': 'True'
        }),
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


    def clean_email(self):
        email = self.cleaned_data.get('email')
        model = self.Meta.model
        user = model.objects.filter(email__iexact=email)

        if user.exists():
            raise forms.ValidationError("A user with that email already exists")

        return self.cleaned_data.get('email')


# Create a ProfileUpdateForm to update image.
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

# class FormChangePassword(PasswordChangeForm):

#     def init(self, args, **kwargs):
#         super(FormChangePassword, self).init(args, **kwargs)
#         for field in ('old_password', 'new_password1', 'new_password2'):
#             self.fields[field].widget.attrs = {'class': 'form-control', 'placeholder': 'Hello'}

class FormChangePassword(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))

    class meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

