from django.contrib import admin
from .models import UserStorageData, Party, UserPartyList, Notification, Kanban, TaskColumns, Tasks

# Register your models here.

admin.site.register(UserStorageData)
admin.site.register(Party)
admin.site.register(UserPartyList)
admin.site.register(Notification)
admin.site.register(Kanban)
admin.site.register(TaskColumns)
admin.site.register(Tasks)