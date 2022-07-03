from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import NewUserForm

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
    return render(request, 'files/files.html')

@login_required
def account(request):
    return render(request, 'files/account.html')

def media_access(request, path):
    access_granted = False
    user = request.user
    return render(request, "files/index.html")
