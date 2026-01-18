from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.http import HttpResponse

def contenttypes_info(request):
    """Info view for contenttypes app"""
    return HttpResponse("ContentTypes app is active. This app provides a framework for tracking models and their relationships.")

def sessions_info(request):
    """Info view for sessions app"""
    return HttpResponse("Sessions app is active. This app provides session management functionality.")

urlpatterns = [
    path("", RedirectView.as_view(url="bookshelf/", permanent=False), name="home"),
    path("bookshelf/", include("bookshelf.urls")),
    path("admin/", admin.site.urls),
    # Authentication URLs (login, logout, password change, etc.)
    path("auth/", include("django.contrib.auth.urls")),
    # ContentTypes and Sessions info endpoints
    path("contenttypes/", contenttypes_info, name="contenttypes_info"),
    path("sessions/", sessions_info, name="sessions_info"),
]