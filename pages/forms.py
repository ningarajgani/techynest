from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile , Address

# Inside forms.py or views.py (wherever the issue is)
def some_view_or_function():
    from .models import Profile  # Import inside the function to avoid circular imports
    # Your code here


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # Edit name (username) and email

class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'profile_picture']

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['locality', 'city', 'state', 'zipcode']
