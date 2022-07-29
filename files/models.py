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
    notifTypes = models.JSONField(null=False, default=["NULL"])
    

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

