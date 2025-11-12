from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'my_admin/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_admin():
            return reverse_lazy('my_admin:dashboard')
        else:
            return reverse_lazy('employees:detail', kwargs={'pk': user.employee.id})
