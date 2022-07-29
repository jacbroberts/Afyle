from django.contrib import admin
from .models import UserStorageData, Party, UserPartyList

# Register your models here.

admin.site.register(UserStorageData)
admin.site.register(Party)
admin.site.register(UserPartyList)