from tokenize import group
from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about),
    path('privacy', views.privacy),
    path('terms', views.terms),
    path('register', views.register),
    path('files', views.files),
    path('account', views.account),
    path('upload', views.upload, name='upload'),
    path('download/<str:username>/<str:filename>', views.download, name='download'),
    path('status', views.status),
    path('groups', views.groups),
    path('groups/<str:name>', views.group_view),
    path('notifications', views.notifications),
    path('kanban/<str:type>/<str:owner>/<str:title>', views.kanban),
    path('kanban/<str:type>/<str:owner>', views.kanbans)
]

