from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import NewUserForm

# Create your views here.

def index(request):
    return render(request, 'files/index.html')
    
def about(request):
    return render(request, 'files/about.html')

def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
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