from django.urls import path
from . import views

app_name = "admin_app"

from . import views
from rest_framework import routers
from django.urls import path, include


urlpatterns = [

    #onion api
    path('sign-in/', views.SignInView, name="sign_in"),
    path('sign-out/', views.SignOutView, name="sign_out"),
    
    path('', views.IndexView, name="index"),

    path('all-problems/', views.AllProblemsView, name="all_problems"),
    path('problem-detail/<int:problem_id>/', views.ProblemDetailView, name="problem_detail"),

    path('all-users/', views.AllUsersView, name="all_users"),
    path('user-detail/<int:user_id>/', views.UserDetailView, name="user_detail"),

    path('approve-solution/<int:solution_id>/', views.ApproveSolutionView, name="approve_solution"),
    path('approve-user/<int:app_user_id>/', views.ApproveUserView, name="approve_user"),
    path('approve-problem/<int:problem_id>/', views.ApproveProblemView, name="approve_problem"),

]

