from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from Insta.models import InstaUser

class CustomUserCreationForm(UserCreationForm):
    #form的原数据
    class Meta(UserCreationForm.Meta):
        model=InstaUser
        fields=('username','email','profile_pic')