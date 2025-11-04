from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .forms import RegisterForm
from .models import User


# ------------------- REGISTER WITH OTP --------------------
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'       # default role
            user.is_active = False      # block login until OTP verified
            user.save()

            # Generate OTP and send
            user.generate_otp()
            send_mail(
                subject="Email Verification OTP",
                message=f"Your OTP is: {user.otp}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )

            request.session['pending_user'] = user.username
            messages.info(request, "OTP sent to your email. Verify to activate account.")
            return redirect('verify_otp')
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def verify_otp(request):
    if request.method == 'POST':
        input_otp = request.POST.get('otp')
        username = request.session.get('pending_user')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Session expired. Register again.")
            return redirect('register')

        if user.otp == input_otp:
            user.is_active = True
            user.otp = None
            user.save()
            messages.success(request, "Account verified! You can now login.")
            return redirect('login')
        else:
            messages.error(request, "Incorrect OTP.")

    return render(request, 'accounts/verify_otp.html')


# ----------------------- LOGIN & LOGOUT ---------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                elif user.role == 'teacher':
                    return redirect('teacher_dashboard')
                else:
                    return redirect('student_dashboard')
            else:
                messages.warning(request, "Verify your email first.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')


def unauthorized(request):
    return render(request, 'accounts/unauthorized.html')


@login_required
def home_redirect(request):
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    elif request.user.role == 'teacher':
        return redirect('teacher_dashboard')
    return redirect('student_dashboard')


# ---------------- PASSWORD RESET (OTP) ---------------------
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No user found with this email.")
            return redirect('forgot_password')

        user.generate_otp()
        send_mail(
            subject="Password Reset OTP",
            message=f"Your OTP to reset password is: {user.otp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        request.session['reset_user'] = user.username
        messages.info(request, "OTP sent to email. Enter OTP to continue.")
        return redirect('verify_reset_otp')

    return render(request, 'accounts/forgot_password.html')


def verify_reset_otp(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        username = request.session.get('reset_user')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Session expired. Try again.")
            return redirect('forgot_password')

        if user.otp == otp_entered:
            user.otp = None
            user.save()
            return redirect('reset_password')

        messages.error(request, "Incorrect OTP.")

    return render(request, 'accounts/verify_reset_otp.html')


def reset_password(request):
    if request.method == 'POST':
        username = request.session.get('reset_user')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password')

        user = User.objects.get(username=username)
        user.set_password(password1)
        user.save()

        # Send confirmation email
        send_mail(
            subject="Password Reset Confirmation",
            message=(
                f"Hello {user.username},\n\n"
                "Your password has been changed successfully.\n"
                "If this wasn't you, contact support immediately.\n\n"
                "Regards,\nTask Management System"
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        messages.success(request, "Password reset successful! Login now.")
        return redirect('login')

    return render(request, 'accounts/reset_password.html')
