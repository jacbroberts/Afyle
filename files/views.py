from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from files.models import UserStorageData, Party, UserPartyList, Notification, Kanban, TaskColumn, Task
from .forms import NewUserForm, UploadFileForm, NewGroupForm, InviteUserToParty, NewKanbanBoard
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
            newUserStorageData = UserStorageData(user=new_user, storage_max_B=10000, bandwidth_upload_max_kB=10000, bandwidth_download_max_kB=10000, files=["NULL"])
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

def write_file(file, user):
    user_storage_data = UserStorageData.objects.get(user__exact=user)
    username = user.get_username()


    #file info
    new_file_name = file.name
    new_file_upload_date = datetime.datetime.now().strftime("%m/%d/%Y")
    new_file_size = int(file.size) #in future, may be rounded to 1kb if file is less than 1000 B
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
def download(request, username, filename):

    
    user = UserStorageData.objects.get(user=request.user)
    #check user's download bandwidth
    if user.bandwidth_download_used_kB >= user.bandwidth_download_max_kB:
        return HttpResponseRedirect('/files')
    
    for file in user.files:
        if str(file['name']) == str(filename) and username == request.user.get_username():
            file_name = file['name']
            response = HttpResponse()
            response['X-Accel-Redirect'] = f'/protected/{user.user}/{file_name}'

            #update download bandwidth
            user.bandwidth_download_used_kB += file['size']/1000

            user.save()


            return response
    
    return HttpResponseRedirect('/files')

@user_passes_test(lambda u:u.is_staff)
def status(request):
    #display: # of users, storage used by users, u/d bandwidth used by users
    # eventually: list of ips, monthly usage (storage/bandwidth/users)
    users = User.objects.all()
    user_count = 0
    for user in users:
        user_count += 1
    
    storage = UserStorageData.objects.all()
    
    storage_used = 0
    upload = 0
    download = 0
    
    for user in storage:
        storage_used += user.storage_used_B
        upload += user.bandwidth_upload_used_kB
        download += user.bandwidth_download_used_kB
    

    return render(request, 'files/status.html', {"user_count": user_count, "storage_used":storage_used, "upload":upload, "download":download})

def is_party_member(user, party_name):
    party = Party.objects.get(name=party_name)
    users_in_party = UserPartyList.objects.filter(party=party)
    try:
        users_in_party.get(user=user)
        return True
    except UserPartyList.DoesNotExist:
        print("invalid user")
        return False


@login_required
def groups(request):
    if request.method == 'POST':
        form = NewGroupForm(request.POST)
        if form.is_valid():
            new_group_name = form.cleaned_data.get("name")
            try:
                Party.objects.get(name=new_group_name)
                print("already exists")
                return render(request, 'files/group_exists.html')
            except Party.DoesNotExist:
                new_group = Party(name=new_group_name)
                new_group.save()
                add_owner = UserPartyList(user=request.user, party=new_group, role="owner")        
                add_owner.save()   
    else:
        form = NewGroupForm()

        groups = UserPartyList.objects.filter(user=request.user)
        parties = []
        for entry in groups:
            parties.append(entry.party.name)
        
    return render(request, 'files/groups.html', {"form":form, "groups":groups})

@login_required
def group_view(request, name):
    party = Party.objects.get(name=name)
    
    user_role_in_group = UserPartyList.objects.filter(user=request.user)
    user_role_in_group = user_role_in_group.get(party=party)
    user_role_in_group = user_role_in_group.role
    
    if request.method == 'POST':
        form = InviteUserToParty(request.POST)
        if user_role_in_group == "owner" or user_role_in_group == "admin":
            pass
    else:
        form = InviteUserToParty()
        try:
            
            users_in_party = UserPartyList.objects.filter(party=party)

        except Party.DoesNotExist:
            return HttpResponseRedirect('/groups')
    return render(request, 'files/group_view.html', {"partyUsers":users_in_party, "form":form, "name":name})

@login_required
def notifications(request):
    if request.method == 'POST':
        pass 
    else:
        notifications = Notification.objects.filter(user=request.user)

    return render(request, 'files/notifications.html', {"notifications":notifications})

@login_required
def kanbans(request, type, owner):
    try:
        if request.method == 'POST':
            form = NewKanbanBoard(request.POST)
            if form.is_valid():
                new_title = form.cleaned_data.get("title")
                
                if type == "user":
                    if Kanban.objects.filter(type=type).filter(user=request.user).get(title=new_title):
                        print("already exists")
                    else:
                        new_kanban = Kanban(type="user", user=request.user, title=new_title, description=form.cleaned_data.get("description"))
                if type == "group" and is_party_member(request.user, owner):
                    if Kanban.objects.filter(type=type).filter(party=Party.get(name=owner)).get(title=new_title):
                        print("already exists")
                    else:
                        new_kanban = Kanban(type="group", party=Party.get(name=owner), title=new_title, description=form.cleaned_data.get("description"))
                        
                new_kanban.save()


        else:
            form = NewKanbanBoard()
            if type == "user":
                kanban = Kanban.objects.filter(user=request.user)
            if type == "group" and is_party_member(request.user, owner):
                party = Party.objects.get(name=owner)
                kanban = Kanban.objects.filter(party=party)
    except Exception as e:
        print(e)
        
    return render(request, 'files/kanbans.html', {"kanbans":kanban, "form":form, "type":type})

@login_required
def kanban(request, type, owner, title):
    try:
        if request.method == 'POST':
            pass 
        else:
            if type == "user":
                kanban = Kanban.objects.filter(user=request.user)
            if type == "group" and is_party_member(request.user, owner):
                kanban = Kanban.objects.filter(party=owner)
            
            kanban = kanban.get(title=title)

            kanban_task_columns = TaskColumn.objects.filter(kanban=kanban)
            kanban_tasks = Task.objects.filter(kanban=kanban)

        return render(request, 'files/kanban.html', {"kanban_columns":kanban_task_columns, "kanban_tasks":kanban_tasks, "owner":owner})
    except Exception as e:
        print(e)