from django import forms
from user.models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['emp_id', 'full_name', 'username', 'phone', 'department', 'working_status']
        widgets = {
            'emp_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Employee ID'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}),
            'working_status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
