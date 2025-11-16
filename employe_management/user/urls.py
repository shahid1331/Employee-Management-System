from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/image/', views.profile_image_update, name='profile_image_update'),
]
