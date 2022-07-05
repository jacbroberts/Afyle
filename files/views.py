from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from files.models import UserStorageData
from .forms import NewUserForm, UploadFileForm
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    return render(request, 'files/index.html')
    
def about(request):
    return render(request, 'files/about.html')

def privacy(request):
    return render(request, 'files/privacy.html')

def terms(request):
    return render(request, 'files/terms_and_conditions.html')

def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            #first check if email is already used
            
            form.save()
            
            #add to UserStorageData class
            new_user = User.objects.get(username__exact=form.cleaned_data.get("username"))
            newUserStorageData = UserStorageData(user=new_user, files=["NULL"])
            newUserStorageData.save()
            
            return redirect("/")
        else:
            #messages.add_message(request, messages.ERROR, "Registration Unsuccessful")
            print("Unsuccessful registration")
    else:
        form = NewUserForm()
    return render(request, 'files/register.html', {"form":form})

#if logged in
@login_required
def files(request):
    user_storage_data = UserStorageData.objects.get(user__exact=request.user)
    return render(request, 'files/files.html', {"userStorage":user_storage_data})

@login_required
def account(request):
    user_storage_data = UserStorageData.objects.get(user__exact=request.user)
    return render(request, 'files/account.html', {"userStorage":user_storage_data})

def media_access(request, path):
    access_granted = False
    user = request.user
    return render(request, "files/index.html")

def write_file(file, user):
    with open("/home/ubuntu/afyle/media/{user}", 'wb+') as destination:
        for chunck in file.chunks():
            destination.write(chunck)

@login_required
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            write_file(request.FILES['file'], request.user.get_username)
            return HttpResponseRedirect('/files')
    else:
        form = UploadFileForm()
        
    return render(request, 'files/upload.html', {"form":form})


