from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about),
    path('register', views.register),
    path('files', views.files),
    path('account', views.account)
]

