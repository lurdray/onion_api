from django.urls import path
from . import views

app_name = "app_user"

from . import views
from rest_framework import routers
from django.urls import path, include


urlpatterns = [

    path('sign-in/', views.SignInView, name="sign_in"),
    path('sign-up/', views.SignUpView, name="sign_up"),
    path('email-verify/', views.EmailVerifyView, name="email_verify"),
    path('sign-out/', views.SignOutView, name="sign_out"),
    
    path('', views.IndexView, name="index"),
    path('profile/', views.ProfileView, name="profile"),
    path('notifications/', views.NotificationsView, name="notifications"),
    path('timeline/', views.TimelineView, name="timeline"),

    path('clap-solution/<int:solution_id>/', views.ClapSolutionView, name="clap_solution"),
    path('buzz-solution/<int:solution_id>/', views.BuzzSolutionView, name="buzz_solution"),

    path('notify/<str:msg>/', views.NotifyView, name="notify"),

    path('add-problem/', views.AddProblemView, name="add_problem"),
    path('problem-detail/<int:problem_id>/', views.ProblemDetailView, name="problem_detail"),

]

