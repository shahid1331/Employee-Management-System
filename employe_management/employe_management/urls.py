from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('my_admin.urls', 'my_admin'), namespace='my_admin')),
    path('user/', include(('user.urls', 'user'), namespace='user')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)