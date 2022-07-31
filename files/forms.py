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
    email = forms.EmailField(required=False)
    name = forms.CharField(required=False)

class NewKanbanBoard(forms.Form):
    title = forms.CharField(required=True, max_length=256)
    description = forms.CharField(required=False, max_length=1024)



archive_method_choices = (
    ("1", "Time after task put into column"),
    ("2", "Task count"),
    ("3", "Time after due"),
)

sort_method_choices = (
    ("1", "Priority"),
    ("2", "Due Date"),
    ("3", "Time Created"),
    ("4", "Alphabetically"),
    ("5", "Manual")
)

class NewKanbanColumn(forms.Form):
    title = forms.CharField(required=True, max_length=256)
    archive_method = forms.ChoiceField(choices=archive_method_choices)
    sort_method = forms.ChoiceField(choices=sort_method_choices)


class NewKanbanTask(forms.Form):
    title = forms.CharField(required=True, max_length=256)
    description = forms.CharField(required=False, max_length=1024)
    due_date = forms.DateField()
    priority = forms.IntegerField(min_value=1, max_value=4, initial=1)