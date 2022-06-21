from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_page, name="start_page"),
    path('login/', views.login_page, name="login_page"),
    path('register/', views.register_page, name="register_page"),
    path('logout/', views.logout_page, name="logout_page"),
]