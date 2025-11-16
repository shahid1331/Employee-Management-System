# user/forms.py
from django import forms
from .models import Employee

class EmployeeRegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ['full_name', 'email', 'username', 'department', 'phone']

    def clean(self):
        cleaned = super().clean()
        pass1 = cleaned.get("password1")
        pass2 = cleaned.get("password2")

        if pass1 != pass2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned


class EditEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'full_name',
            'email',
            'department',
            'phone',
            'image',        # <--- REQUIRED FOR UPLOAD
            'job_title',
            'birthday',
            'joining_date',
        ]
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }
