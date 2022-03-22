from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Chat.urls')),

    path('login/', auth_views.LoginView.as_view(template_name='Chat/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='Chat/logout.html'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 