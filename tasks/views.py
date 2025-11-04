# tasks/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from .models import Task
from .forms import TaskForm
from accounts.models import User


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('unauthorized')

    # Handle deletion actions
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
        'users': users
    })


@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return redirect('unauthorized')

    tasks = Task.objects.filter(created_by=request.user).order_by('-id')

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)

        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            form.save_m2m()   # Save many-to-many assigned students

            # Send email to each assigned student
            for student in task.assigned_to.all():
                send_mail(
                    subject=f"New Task Assigned: {task.title}",
                    message=(
                        f"Hello {student.username},\n\n"
                        f"You have been assigned a new task by {request.user.username}.\n"
                        f"Task: {task.title}\n"
                        f"Deadline: {task.deadline if task.deadline else 'No deadline'}\n\n"
                        f"Description:\n{task.description}\n\n"
                        "Please login to the system to complete the task.\n\n"
                        "Regards,\nTask Management System"
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[student.email],
                    fail_silently=False,
                )

            messages.success(request, "Task created & students notified!")
            return redirect('teacher_dashboard')
        else:
            messages.error(request, "Something went wrong. Check your form.")

    else:
        form = TaskForm()
        # Show only students as assignable users
        form.fields['assigned_to'].queryset = User.objects.filter(role='student')

    return render(request, 'tasks/teacher_dashboard.html', {
        'tasks': tasks,
        'form': form
    })


@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('unauthorized')

    tasks = Task.objects.filter(assigned_to=request.user).order_by('-id')

    return render(request, 'tasks/student_dashboard.html', {
        'tasks': tasks
    })

@login_required
@permission_required('tasks.can_create_task', raise_exception=True)
def student_create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            form.save_m2m()
            messages.success(request, "Task created successfully!")
            return redirect('student_dashboard')
    else:
        form = TaskForm()

    return render(request, 'tasks/student_create_task.html', {'form': form})
