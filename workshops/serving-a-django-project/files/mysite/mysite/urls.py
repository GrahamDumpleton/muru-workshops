"""URL configuration for mysite project."""

from django.contrib import admin
from django.urls import path

from catalog import views

urlpatterns = [
    path("", views.index),
    path("stock", views.stock),
    path("ping", views.ping),
    path("admin/", admin.site.urls),
]
