"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import my_app
from my_app import views

urlpatterns = [
    path('', views.home, name='home'),

    path('admin/', admin.site.urls),

    path('tasks/', my_app.views.task_list, name='task_list'),

    path("create/", views.task_create, name='task_create'),

    path("register/", views.user_register, name='user_register'),

    path('profile-setup/', views.profile_setup, name='profile_setup'),

    path("login/", views.user_login, name='user_login'),

    path("logout/", views.user_logout, name='user_logout'),

    path('claim-task/<int:task_id>/', views.claim_task, name='claim_task'),

    path('complete-task/<int:task_id>/', views.complete_task, name='complete_task'),

    path('task_delete/<int:task_id>/', views.task_delete, name='task_delete'),

    path('task/edit/<int:task_id>/', views.task_edit, name='task_edit'),

]
