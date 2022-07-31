from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import datetime

# Create your models here.

class UserStorageData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    dynamic_max = models.BooleanField(default=True)
    
    storage_used_B = models.PositiveBigIntegerField(default=0) #upto 9,223,372,036,854,775,807 B
    storage_max_B = models.PositiveBigIntegerField(default=0)
    
    bandwidth_upload_used_kB = models.FloatField(default=0)
    bandwidth_upload_max_kB = models.FloatField(default=0)
    
    bandwidth_download_used_kB = models.FloatField(default=0)
    bandwidth_download_max_kB = models.FloatField(default=0)

    files = models.JSONField(null=False, default=list)

    notificationsOn = models.BooleanField(default=True)
    notifTypes = models.JSONField(null=False, default=list)

    task_count = models.PositiveBigIntegerField(default=0)


    def __str__(self):
        return self.user.username

# files =[
#     {
#         "name": "name",
#         "upload_date": "jdl"
#         "size": "size",
#         "type": "type"

class Party(models.Model):
    name = models.CharField(max_length=256)
    joinHow = models.CharField(default="invite", max_length=256)
    codeHash = models.CharField(default="NULL", max_length=256)
    codeSalt = models.CharField(default="NULL", max_length=256)

    def __str__(self):
        return self.name


class UserPartyList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    party = models.OneToOneField(Party, on_delete=models.CASCADE)
    role = models.CharField(default="member", max_length=256)
    date_joined = models.DateTimeField(default=timezone.now)

class Notification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    priority = models.PositiveIntegerField(default=1)
    type = models.CharField(max_length=256)
    time = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=1024)
    is_read = models.BooleanField(default=False)

class Kanban(models.Model):
    type = models.CharField(max_length=16)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    party = models.ForeignKey(Party, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=1024)

    def __str__(self):
        if self.type == "user":
            return f"{self.user}:{self.title}"
        elif self.type == "group":
            return f"{self.group}:{self.title}"
        else:
            return f"{self.title}"

class TaskColumn(models.Model):
    kanban = models.ForeignKey(Kanban, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    state = models.CharField(max_length=256, default="active")
    do_sort = models.BooleanField(default=False)
    sort_by = models.CharField(max_length=16, default="M")
    do_auto_archive = models.BooleanField(default=False)
    archive_by = models.CharField(max_length=256, blank=True, null=True)
    task_count = models.PositiveBigIntegerField(default=0)
    archived_date = models.DateTimeField(blank=True, null=True)
    trash_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{str(self.kanban)}:{self.title}"

class Task(models.Model):
    kanban = models.ForeignKey(Kanban, on_delete=models.CASCADE)
    column = models.ForeignKey(TaskColumn, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=1024)
    state = models.CharField(max_length=256, default="active")
    do_auto_archive = models.BooleanField(default=False)
    archive_by = models.CharField(max_length=256, blank=True, null=True)
    timeToArchive = models.DateTimeField(blank=True, null=True)
    countToArchive = models.PositiveIntegerField(default=-1)
    priority = models.PositiveIntegerField(default=1)
    date_recorded = models.DateTimeField(default=timezone.now)
    date_due = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{str(self.column)}:{self.title}"
