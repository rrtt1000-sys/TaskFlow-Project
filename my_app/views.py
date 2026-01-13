from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseForbidden

from .Forms.FilterForm import TaskFilterForm
from .Forms.SetProfile import ProfileForm
from .models import Task, Profile
from .Forms.AddTask import TaskForm
from .Forms.Registerform import RegisterForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404


def home(request):
    return render(request, 'home.html')


@transaction.atomic
def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.save()
            login(request, user)
            return redirect('profile_setup')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task_list')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required
def profile_setup(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    # יצירת פרןפיל חדש (אם יש)
    if request.method == "POST":
        # instance=profile מעדכן את הפרופיל הקיים במקום ליצור אחד חדש
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        # טעינת הטופס עם הנתונים הקיימים (אם יש)
        form = ProfileForm(instance=profile)

    return render(request, 'Profile.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


# @login_required
# def task_list(request):
# user_team = request.user.profile.Team
#    tasks = Task.objects.filter(Team=user_team)
#  return render(request, 'Task_List.html', {'tasks': tasks})


@login_required
def task_create(request):
    if request.user.profile.role != 'manager':
        messages.error(request, "גישה נדחתה: רק מנהל יכול להוסיף משימות.")
        return redirect('task_list')
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.Team = request.user.profile.Team
            task.status = 'New'
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'task_form.html', {'form': form})


@login_required
def claim_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if task.Team == request.user.profile.Team and task.profile is None:
        task.profile = request.user.profile
        task.status = 'IN_PROGRESS'
        task.save()

    return redirect('task_list')


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, profile=request.user.profile)
    task.status = 'COMPLETED'
    task.save()
    return redirect('task_list')


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user.profile.role == 'manager' and task.Team == request.user.profile.Team:
        task.delete()
        return redirect('task_list')
    else:
        return HttpResponseForbidden("אין לך הרשאה למחוק משימה זו.")


@login_required
def task_list(request):
    profile = request.user.profile
    tasks = Task.objects.filter(Team=profile.Team)

    form = TaskFilterForm(request.GET or None)

    if form.is_valid():
        if form.cleaned_data['status']:
            tasks = tasks.filter(status=form.cleaned_data['status'])

        if form.cleaned_data['worker']:
            tasks = tasks.filter(
                profile__user__username__icontains=form.cleaned_data['worker']
            )

    return render(request, 'Task_List.html', {
        'tasks': tasks,
        'form': form
    })


@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user.profile.role != 'manager' or task.profile is not None:
        return HttpResponseForbidden("אינך מורשה לערוך משימה זו (או שהיא כבר משויכת לעובד).")

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'task_form.html', {'form': form, 'title': 'עריכת משימה'})