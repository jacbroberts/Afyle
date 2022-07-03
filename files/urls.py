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
    path(r'media/(?P<path>.*', views.media_access, name='media'),
]

