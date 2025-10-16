from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("",index,name='index'),
    path("register",RegisterView.as_view(),name='register'),
    path("register-list",RegisterListView.as_view(),name="register-list"),
    path("login",LoginView.as_view(),name="login-view"),
    path("dashboard/", DashboardView.as_view(), name='dashboard-page'),
    path("job-detail/",JobDetailView.as_view(),name='job_detail'),
    path("job-list/<uuid:pk>/",JobUpdateDelete.as_view(),name='job-list')
    
    
]
