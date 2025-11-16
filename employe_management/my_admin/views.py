from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from user.models import Employee
from .forms import EmployeeForm

def staff_required(user):
    return user.is_active and user.is_staff

@login_required
@user_passes_test(staff_required)
def employee_list(request):
    employees = Employee.objects.all().order_by('id')
    return render(request, 'employee_list.html', {'employees': employees})

@login_required
@user_passes_test(staff_required)
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES or None)
        if form.is_valid():
            emp = form.save()
            messages.success(request, f'Employee "{emp.full_name}" added successfully.')
            return redirect('my_admin:employee-list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form, 'title': 'Add Employee'})

@login_required
@user_passes_test(staff_required)
def employee_update(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES or None, instance=emp)
        if form.is_valid():
            emp = form.save()
            messages.success(request, f'Employee "{emp.full_name}" updated successfully.')
            return redirect('my_admin:employee-list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = EmployeeForm(instance=emp)
    return render(request, 'employee_form.html', {'form': form, 'title': 'Edit Employee', 'employee': emp})

@login_required
@user_passes_test(staff_required)
def employee_delete(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        emp.delete()
        messages.success(request, f'Employee "{emp.full_name}" deleted.')
        return redirect('my_admin:employee-list')
    return render(request, 'employee_confirm_delete.html', {'employee': emp})

@login_required
@user_passes_test(staff_required)
def employee_toggle_block(request, pk):
    """
    Toggle block/unblock — we use the employee.working_status boolean
    True -> Active, False -> Inactive. If your model has 'is_active', update accordingly.
    """
    emp = get_object_or_404(Employee, pk=pk)
    emp.working_status = not bool(emp.working_status)
    emp.save()
    state = "unblocked" if emp.working_status else "blocked"
    messages.success(request, f'Employee "{emp.full_name}" is now {state}.')
    return redirect('my_admin:employee-list')

@login_required
@user_passes_test(staff_required)
def admin_dashboard(request):
    total_employees = Employee.objects.count()
    active_count = Employee.objects.filter(working_status=True).count()
    inactive_count = total_employees - active_count
    recent_employees = Employee.objects.order_by('-id')[:10]

    return render(request, 'admin_dashboard.html', {
        'total_employees': total_employees,
        'active_count': active_count,
        'inactive_count': inactive_count,
        'recent_employees': recent_employees,
    })
