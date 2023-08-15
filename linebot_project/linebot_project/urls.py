from django.contrib import admin
from django.urls import path
from linebot_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("callback/", views.callback),
    path("", views.index),
]
