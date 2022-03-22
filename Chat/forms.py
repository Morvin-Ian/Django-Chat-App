from dataclasses import fields
from django import forms
from django.forms import ModelForm
from .models import ChatRoom, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [ 'username','email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['room_title', 'name','description']

class UpdateDetails(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [ 'username','email']

class UpdateProfile(forms.ModelForm):
   class Meta:
       model = Profile
       fields = ['profile_pic']