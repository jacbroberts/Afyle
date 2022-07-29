from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UploadFileForm(forms.Form):
    file = forms.FileField(required=True)


class NewGroupForm(forms.Form):
   name = forms.CharField(required=True)


class InviteUserToParty(forms.Form):
    email = forms.EmailField()
    name = forms.CharField()