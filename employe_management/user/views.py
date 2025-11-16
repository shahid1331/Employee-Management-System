# user/views.py
import traceback
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import EmployeeRegisterForm, EditEmployeeForm
from .models import Employee

User = get_user_model()

# ---------------------------
# Registration & profile ops
# ---------------------------
def register(request):
    debug = {}

    if request.method == "POST":
        form = EmployeeRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            full_name = form.cleaned_data.get('full_name', '')
            department = form.cleaned_data.get('department', '')
            phone = form.cleaned_data.get('phone', '')

            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

                try:
                    user.full_name = full_name
                    user.department = department
                    user.phone = phone
                    user.save()
                except Exception:
                    # best-effort, not critical
                    pass

                try:
                    emp, created = Employee.objects.update_or_create(
                        username=username,
                        defaults={
                            'full_name': full_name,
                            'email': email,
                            'department': department,
                            'phone': phone,
                        }
                    )
                except Exception:
                    pass

                messages.success(request, "Account created successfully. Please login.")
                return redirect('my_admin:login')

            except Exception as e:
                debug["create_user_error"] = str(e)
                debug["traceback"] = traceback.format_exc()

                try:
                    emp = Employee.objects.create(
                        full_name=full_name,
                        email=email,
                        username=username,
                        department=department,
                        phone=phone,
                        password=make_password(password),
                    )
                    messages.success(request, "Account created. Please login.")
                    return redirect('my_admin:login')

                except Exception as e2:
                    debug["fallback_error"] = str(e2)
                    debug["fallback_traceback"] = traceback.format_exc()
                    messages.error(request, "Account creation failed. See debug below.")

        else:
            debug["form_errors"] = form.errors.as_json()
            messages.error(request, "Please fix the form errors.")
    else:
        form = EmployeeRegisterForm()

    return render(request, "register.html", {"form": form, "debug": debug})


@login_required
def profile_view(request):
    """
    View the logged-in user's Employee profile.
    """
    try:
        emp = Employee.objects.get(username=request.user.username)
    except Employee.DoesNotExist:
        emp = None

    return render(request, "userdetails.html", {"employee": emp, "object": emp})


@login_required
def profile_edit(request):
    """
    Edit the logged-in user's Employee profile (handles file upload).
    """
    try:
        emp = Employee.objects.get(username=request.user.username)
    except Employee.DoesNotExist:
        emp = None

    if request.method == "POST":
        form = EditEmployeeForm(request.POST, request.FILES, instance=emp)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('user:profile')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = EditEmployeeForm(instance=emp)

    return render(request, "user_profile_edit.html", {"form": form, "employee": emp})


@login_required
def profile_image_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect('my_admin:dashboard')

    uploaded = request.FILES.get('image')
    # debug: print what arrived
    print("=== profile_image_update DEBUG ===")
    print("request.FILES keys:", list(request.FILES.keys()))
    print("uploaded object:", repr(uploaded))
    if uploaded:
        try:
            print("filename:", uploaded.name)
            print("size:", getattr(uploaded, 'size', 'unknown'))
            print("content_type:", getattr(uploaded, 'content_type', 'unknown'))
        except Exception as e:
            print("error inspecting uploaded:", e)
            traceback.print_exc()

    if not uploaded:
        messages.error(request, "No image uploaded. (server debug printed).")
        return redirect('my_admin:dashboard')

    # temporary accept everything and save (for debugging)
    try:
        emp, _ = Employee.objects.get_or_create(
            username=request.user.username,
            defaults={
                'full_name': getattr(request.user, 'full_name', request.user.username),
                'email': getattr(request.user, 'email', '')
            }
        )
        emp.image = uploaded
        emp.save()
        messages.success(request, f"Uploaded {uploaded.name} ({uploaded.size} bytes). Check server console for debug.")
    except Exception as e:
        print("save error:", e)
        traceback.print_exc()
        messages.error(request, "Saving failed (see server console).")

    return redirect('my_admin:dashboard')

# ---------------------------
# Authentication views (ADDED)
# ---------------------------
def login_user(request):
    """
    Login view using Django's AuthenticationForm.
    - staff -> my_admin:employee-list
    - non-staff -> my_admin:dashboard (your project maps dashboard to user_dashboard under my_admin namespace)
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect based on staff status
            if user.is_staff:
                return redirect('my_admin:employee-list')
            return redirect('my_admin:dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm(request)

    return render(request, "login.html", {"form": form})


@login_required
def user_dashboard(request):
    """
    Dashboard view for regular users.
    This will be used by my_admin.urls if you map it there (as your current URLs expect).
    """
    try:
        emp = Employee.objects.get(username=request.user.username)
    except Employee.DoesNotExist:
        emp = None

    # choose template name dashboard.html — adjust if you prefer userdetails.html
    return render(request, "dashboard.html", {"employee": emp})


def logout_view(request):
    """
    Log the user out and redirect to the login page.
    """
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('my_admin:login')
