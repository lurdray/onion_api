from django.urls import path
from . import views

app_name = "admin_app"

from . import views
from rest_framework import routers
from django.urls import path, include


urlpatterns = [

    #onion api
    
    path('confirm-payment/', views.ConfirmPaymentView, name="confirm_payment"),
    
    path('', views.SignInView, name="sign_in"),
    path('sign-out/', views.SignOutView, name="sign_out"),
    
    path('index/', views.IndexView, name="index"),
    
    path('all-categories/', views.AllCategoriesView, name="all_categories"),
    path('category-detail/<int:category_id>/', views.CategoryDetailView, name="category_detail"),
    path('delete/category/<int:category_id>/', views.DeleteCategoryView, name="delete_category"),



    path('all-problems/', views.AllProblemsView, name="all_problems"),
    path('problem-detail/<int:problem_id>/', views.ProblemDetailView, name="problem_detail"),

    path('all-problems/', views.AllProblemsView, name="all_problems"),
    path('problem-detail/<int:problem_id>/', views.ProblemDetailView, name="problem_detail"),

    path('all-reported-videos/', views.ReportedVideosView, name="reported_videos"),

    path('reported-problem-detail/<int:problem_id>/', views.ReportPDetailView, name="reported_p_detail"),
    path('reported-solution-detail/<int:solution_id>/', views.ReportSDetailView, name="reported_s_detail"),

    path('all-users/', views.AllUsersView, name="all_users"),
    path('user-detail/<int:user_id>/', views.UserDetailView, name="user_detail"),

    path('approve-solution/<int:solution_id>/', views.ApproveSolutionView, name="approve_solution"),
    path('approve-user/<int:app_user_id>/', views.ApproveUserView, name="approve_user"),
    path('approve-problem/<int:problem_id>/', views.ApproveProblemView, name="approve_problem"),

]

