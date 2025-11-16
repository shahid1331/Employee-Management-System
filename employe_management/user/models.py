from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    job_title = models.CharField(max_length=150, blank=True)
    birthday = models.DateField(null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    emp_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    working_status = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name
