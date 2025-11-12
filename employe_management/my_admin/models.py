from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        Employee = 'EMPLOYEE', 'Employee'
        
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.Employee)
    
    def is_admin(self):
        return self.role == self.Roles.ADMIN