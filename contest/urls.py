from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_page, name="start_page"),
    path('login/', views.login_page, name="login_page"),
    path('register/', views.register_page, name="register_page"),
    path('logout/', views.logout_page, name="logout_page"),
    path('profile/', views.profile_page, name="profile_page"),
    path('contest_creation/', views.contestcreator_page, name="contestcreator_page"),
    path('contest_update/<str:pk>', views.contestupdate_page, name="contestupdate_page"),
    path('contest_delete/<str:pk>', views.contestdelete_page, name="contestdelete_page"),
    path('add_user/<str:pk>', views.add_page, name="add_page"),
    path('view/<str:pk>', views.view_page, name="view_page"),
    path('start_contest/<str:pk>', views.startcontest_page, name="startcontest_page"),
    path('add_match/<str:pk>', views.add_match, name="add_match"),
    path('end_tournament/<str:pk>', views.end_match, name="end_match")
]