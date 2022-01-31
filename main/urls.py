from django.urls import path
from . import views

app_name = "main"

from . import views
from rest_framework import routers
from django.urls import path, include


urlpatterns = [
    
    #landing page
    path('', views.IndexView, name="index"),
    path('privacy-policy/', views.PrivacyView, name="privacy"),
    path('contact', views.ContactView, name="contact"),
    path('faq/', views.FaqView, name="faq"),

    #onion api
    path('sign-up/', views.SignUpView),
    path('sign-in/', views.SignInView),

    path('get-appuser/<str:auth_code>/', views.ACGetAppUserView),
    path('edit-appuser/', views.EditAppUserView),

    path('add-problem/', views.AddProblemView),
    path('edit-problem/', views.EditProblemView),
    path('add-solution/', views.AddSolutionView),

    path('set-payment/', views.SetPaymentView),

    path('get-user-problems/<str:auth_code>/', views.GetUserProblemsView),
    path('get-user-solutions/<str:auth_code>/', views.GetUserSolutionsView),
    path('get-problem-solutions/<int:problem_id>/', views.GetProblemSolutionsView),

    path('get-all-problems/', views.GetAllProblemsView),
    path('get-all-solutions/', views.GetAllSolutionsView),
    
    path('get-problem-detail/<str:auth_code>/<int:problem_id>/', views.GetProblemDetailView),
    path('get-solution-detail/<str:auth_code>/<int:solution_id>/', views.GetSolutionDetailView),

    path('problem/add-clap/', views.AddProblemClapView),
    path('problem/add-buzz/', views.AddProblemBuzzView),
    path('problem/add-comment/', views.AddPCommentView),
    path('problem/get-comments/<int:problem_id>/', views.GetPCommentView),

    path('problem/report/', views.ReportProblemView),
    path('solution/report/', views.ReportSolutionView),

    path('solution/add-clap/', views.AddSolutionClapView),
    path('solution/add-buzz/', views.AddSolutionBuzzView),
    path('solution/add-comment/', views.AddSCommentView),
    path('solution/get-comments/<int:solution_id>/', views.GetSCommentView),

    path('problem/add-rating/', views.RateProblemView),
    path('solution/add-rating/', views.RateSolutionView),

    path('appuser/request/new-password/', views.RequestNewPwView),
    path('appuser/set/new-password/', views.SetNewPwView),
    path('appuser/activate/', views.ActivateUserView),

    path('get-all-tags/', views.GetAllTagView),
    path('get-all-categories/', views.GetAllCategoriesView),
    
    
    path('find-all-problems/tag/', views.FindAllProblemsTView),
    path('find-all-problems/category/', views.FindAllProblemsCView),
    path('find-all-problems/title/', views.FindAllProblemsTiView),
    
    path('get-timeline/', views.GetTimelineView),
    path('get-notifications/<str:auth_code>/', views.GetAppUserNotificationView),

    path('analytics/video-rating/', views.AnalyticsVRView),
    path('analytics/views/', views.AnalyticsVView),
    path('analytics/total-videos/', views.AnalyticsTVView),

    path('analytics/video-rating/<str:auth_code>/', views.AnalyticsUVRView),
    path('analytics/views/<str:auth_code>/', views.AnalyticsUVView),
    path('analytics/total-videos/<str:auth_code>/', views.AnalyticsUTVView),


]

