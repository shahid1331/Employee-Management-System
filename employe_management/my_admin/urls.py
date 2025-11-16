from django.urls import path
from . import views            # my_admin-specific views (employee_list, create, update, ...)
from user.views import (       # import login/dashboard/logout from user app
    login_user as user_login_view,
    user_dashboard as user_dashboard_view,
    logout_view as user_logout_view,
)

app_name = "my_admin"

urlpatterns = [
    # Login Routes (use the views from user.views)
    path('', user_login_view, name='login'),
    path('login/', user_login_view, name='login_alt'),

    # User Dashboard (regular user)
    path('dashboard/', user_dashboard_view, name='dashboard'),

    # Logout
    path('logout/', user_logout_view, name='logout'),

    # Employee List Page (and admin CRUD - from my_admin.views)
    path('employees/', views.employee_list, name='employee-list'),
    path('employees/add/', views.employee_create, name='employee-add'),
    path('employees/<int:pk>/edit/', views.employee_update, name='employee-edit'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee-delete'),
    path('employees/<int:pk>/toggle-block/', views.employee_toggle_block, name='employee-toggle-block'),

    # Admin dashboard (avoid '/admin/...', use a safe path)
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
]
