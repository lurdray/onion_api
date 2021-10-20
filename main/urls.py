from django.urls import path
from . import views

app_name = "main"

from . import views
from rest_framework import routers
from django.urls import path, include


urlpatterns = [

    #onion api
    path('sign-up/', views.SignUpView),
    path('sign-in/', views.SignInView),

    path('get-appuser/<int:app_user_id>/', views.GetAppUserView),
    path('edit-appuser/', views.EditAppUserView),

    path('add-problem/', views.AddProblemView),
    path('edit-problem/', views.EditProblemView),
    path('add-solution/', views.AddSolutionView),


    path('get-user-problems/<int:app_user_id>/', views.GetUserProblemsView),
    path('get-user-solutions/<int:app_user_id>/', views.GetUserSolutionsView),
    path('get-problem-solutions/<int:problem_id>/', views.GetProblemSolutionsView),

    path('get-all-problems/', views.GetAllProblemsView),
    path('get-all-solutions/', views.GetAllSolutionsView),

    path('problem/add-clap/', views.AddProblemClapView),
    path('problem/add-buzz/', views.AddProblemBuzzView),

    path('solution/add-clap/', views.AddSolutionClapView),
    path('solution/add-buzz/', views.AddSolutionBuzzView),

    path('solution/add-rating/', views.RateSolutionView),

    path('appuser/request/new-password/', views.RequestNewPwView),
    path('appuser/set/new-password/', views.SetNewPwView),
    path('appuser/activate/', views.ActivateUserView),

]

