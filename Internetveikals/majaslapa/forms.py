from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Profile

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
