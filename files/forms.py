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

    

#         "name": "name",
#         "upload_date": "jdl"
#         "size": "size",
#         "type": "type"