from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from .models import User


def register(request):
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.role = 'student'  # default role
            new_user.is_active = False  # wait for admin approval
            new_user.save()

            messages.info(
                request,
                "Your registration request has been submitted. Please wait for admin approval."
            )
            return redirect('login')
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                elif user.role == 'teacher':
                    return redirect('teacher_dashboard')
                elif user.role == 'student':
                    return redirect('student_dashboard')
            else:
                messages.warning(request, " Your account is pending admin approval.")
        else:
            messages.error(request, " Invalid username or password.")
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You’ve been logged out successfully.")
    return redirect('login')


def unauthorized(request):
    return render(request, 'accounts/unauthorized.html')


@login_required
def home_redirect(request):
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    elif request.user.role == 'teacher':
        return redirect('teacher_dashboard')
    elif request.user.role == 'student':
        return redirect('student_dashboard')
    return redirect('login')
