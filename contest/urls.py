from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name="login_page"),
    path('dashboard/', views.start_page, name="start_page"),
    path('register/', views.register_page, name="register_page"),
]