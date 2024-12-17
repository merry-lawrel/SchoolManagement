from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


# Extend default User model if needed
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('librarian', 'Librarian'),
    ]
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Staff')

    def set_password(self, raw_password):
        """
        Override the default set_password method to hash the password.
        This is automatically handled by Django's User model, but if needed 
        we can explicitly use it here.
        """
        super().set_password(raw_password)

    def save(self, *args, **kwargs):
        if self.pk is None and self.password:
            self.set_password(self.password)  # Ensure the password is hashed
        super().save(*args, **kwargs)

class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    student_class = models.CharField(max_length=50)
    division = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return self.name

class Staff(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='staff')
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    department = models.CharField(max_length=100)

class Librarian(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='librarian')
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)


class LibraryHistory(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('lost', 'Lost'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student')
    book_name = models.CharField(max_length=200)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return self.book_name


class FeeRecords(models.Model):
    FEE_TYPE_CHOICES = [
        ('tuition', 'Tuition'),
        ('library', 'Library'),
        ('transport', 'Transport'),
        ('exam', 'Exam'),
        ('miscellaneous', 'Miscellaneous'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee_records')
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} - {self.fee_type}"
