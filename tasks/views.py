from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm
from accounts.models import User

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('unauthorized')

    tasks = Task.objects.all()
    users = User.objects.all()
    return render(request, 'tasks/admin_dashboard.html', {
        'tasks': tasks,
        'users': users
    })



@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return redirect('unauthorized')

    # Show all tasks created by this teacher
    tasks = Task.objects.filter(created_by=request.user).order_by('-id')

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user    
            task.save()
            messages.success(request, "Task created successfully!")
            return redirect('teacher_dashboard')
        else:
            messages.error(request, "Please check the form — something went wrong.")
    else:
        form = TaskForm()

    return render(request, 'tasks/teacher_dashboard.html', {
        'tasks': tasks,
        'form': form
    })



@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('unauthorized')

    # Show all tasks assigned to this student
    tasks = Task.objects.filter(assigned_to=request.user).order_by('-id')
    return render(request, 'tasks/student_dashboard.html', {
        'tasks': tasks
    })
# tasks/views.py
@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('unauthorized')

    from accounts.models import User

    # Handle deletions (if requested)
    if request.method == 'POST':
        if 'delete_user' in request.POST:
            user_id = request.POST.get('delete_user')
            User.objects.filter(id=user_id).delete()
            messages.success(request, "User deleted successfully.")
        elif 'delete_task' in request.POST:
            task_id = request.POST.get('delete_task')
            Task.objects.filter(id=task_id).delete()
            messages.success(request, "Task deleted successfully.")
        return redirect('admin_dashboard')

    tasks = Task.objects.all().order_by('-id')
    users = User.objects.all().order_by('id')

    return render(request, 'tasks/admin_dashboard.html', {
        'tasks': tasks,
        'users': users,
    })
