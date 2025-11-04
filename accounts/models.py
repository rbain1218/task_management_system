from django.contrib.auth.models import AbstractUser
from django.db import models
import random

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_active = models.BooleanField(default=False) 

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()


    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


def save(self, *args, **kwargs):
    # Auto assign permissions based on role
    if self.role == "admin":
        self.is_staff = True
        self.is_superuser = True
    elif self.role == "teacher":
        self.is_staff = True
        self.is_superuser = False
    else:  # student
        self.is_staff = False
        self.is_superuser = False

    super(User, self).save(*args, **kwargs)