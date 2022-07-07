from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from files.models import UserStorageData
from .forms import NewUserForm, UploadFileForm
from django.contrib.auth.models import User

import datetime

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

            #create directory in /home/ubuntu/afyle/media/<username>
            
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

def revalidate_storage():
    #check that actual storage usage matches db 
    pass



def write_file(file, user):
    user_storage_data = UserStorageData.objects.get(user__exact=user)
    username = user.get_username()


    #file info
    new_file_name = file.name
    new_file_upload_date = datetime.datetime.now().strftime("%m/%d/%Y")
    new_file_size = int(file.size)
    new_file_type = str(file.content_type)

    new_file_entry = {
        "name": new_file_name,
        "upload_date": new_file_upload_date,
        "size": new_file_size,
        "type": new_file_type
    }

    user_storage_data.storage_used_B += new_file_size
    user_storage_data.bandwidth_upload_used_kB += new_file_size/1000
    
    if user_storage_data.files[0] == "NULL":
        del user_storage_data.files[0]
    user_storage_data.files.append(new_file_entry)
    
    user_storage_data.save()
    
    
    with open(f"/home/ubuntu/afyle/media/{username}/{file.name}", 'wb+') as destination:
        for chunck in file.chunks():
            destination.write(chunck)

@login_required
def upload(request):
    user_storage_data = UserStorageData.objects.get(user__exact=request.user)
    allow_upload = True
    
    #check that user has not surpased upload bandwidth quota
    bandwidth_used = user_storage_data.bandwidth_upload_used_kB
    bandwidth_max = user_storage_data.bandwidth_upload_max_kB
    if bandwidth_used >= bandwidth_max: 
        #upload is still allowed if the current file will go over upload quota
        allow_upload = False
        

    #check that user has not surpased storage usage quota
    storage_used = user_storage_data.storage_used_B
    storage_max = user_storage_data.storage_max_B
    if storage_used >= storage_max:
        #upload still allowed if the current file will go over storage quota
            #after file size is checked, however, file will be discarded
        allow_upload = False
        

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #check that file size does not violate storage quota
            if storage_used + request.FILES['file'].size >= storage_max:
                allow_upload = False
            
            if allow_upload == True:
                write_file(request.FILES['file'], request.user)
                return HttpResponseRedirect('/files')
        
        else:
            print("invalid form sent")
    
    else:
        form = UploadFileForm()
        
    return render(request, 'files/upload.html', {"form":form, "uploadAllowed":allow_upload})


@login_required
def download(request):
    #check that user has not surpased download bandwidth
    pass
