from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("",index,name='index'),
    path("register",RegisterView.as_view(),name='register'),
    path("register-list",RegisterListView.as_view(),name="register-list"),
    path("login",Loginview.as_view(),name="login-view"),
    path("dashboard/", DashboardView.as_view(), name='dashboard-page')

    
]
