from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from main.models import *

# Create your views here.



def SignInView(request):

	if request.method == "POST":
		

		return HttpResponseRedirect(reverse("admin:index"))
		
	else:

		context = {}
		return render(request, "admin_app/sign_in.html", context)




def SignOutView(request):
	logout(request)

	return HttpResponseRedirect(reverse("admin_app:index"))

		




def IndexView(request):

	if request.method == "POST":
		pass

		
	else:

		app_users = AppUser.objects.all()
		problems = Problem.objects.all()
		solutions = Solution.objects.all()
		approved_solutions = Solution.objects.filter(status=True)

		latest_problems = problems[:10]
		latest_users = app_users[:10]
		latest_solution_video = solutions[:10]


		context = {
			"app_users": app_users,
			"problems": problems,
			"solutions": solutions,
			"approved_solutions": approved_solutions,

			"latest_problems": latest_problems,
			"latest_users": latest_users,
			"latest_solution_video": latest_solution_video,

		}

		return render(request, "admin_app/index.html", context)




def AllProblemsView(request):

	if request.method == "POST":
		pass

		
	else:

		problems = Problem.objects.all().order_by("-pub_date")

		context = {
		"problems": problems
		}

		return render(request, "admin_app/all_problems.html", context)


def ProblemDetailView(request, problem_id):

	if request.method == "POST":
		pass

		
	else:
		problem = Problem.objects.get(id=problem_id)
		solutions = Solution.objects.filter(problem__id=problem_id)

		context = {
			"problem": problem, 
			"solutions": solutions,
			}

		return render(request, "admin_app/problem_detail.html", context)



def AllUsersView(request):

	if request.method == "POST":
		pass

		
	else:

		app_users = AppUser.objects.all().order_by("-pub_date")

		context = {
			"app_users": app_users,
		}

		return render(request, "admin_app/all_users.html", context)


def UserDetailView(request, user_id):

	if request.method == "POST":
		pass

		
	else:

		context = {}
		return render(request, "admin_app/user_detail.html", context)





def ApproveSolutionView(request, solution_id):
	if request.method == "POST":

		solution = Solution.objects.get(id=solution_id)
		problem_id = solution.problem.id

		if solution.status == True:
			solution.status = False

		else:
			solution.status = True

		solution.save()

		return HttpResponseRedirect(reverse("admin_app:problem_detail", args=[problem_id,]))



	else:
		pass



def ApproveUserView(request, app_user_id):
	if request.method == "POST":

		app_user = AppUser.objects.get(id=app_user_id)

		if app_user.status == True:
			app_user.status = False

		else:
			app_user.status = True

		app_user.save()

		return HttpResponseRedirect(reverse("admin_app:all_users"))



	else:
		pass	




def ApproveProblemView(request, problem_id):
	if request.method == "POST":

		problem = Problem.objects.get(id=problem_id)

		if problem.status == True:
			problem.status = False

		else:
			problem.status = True

		problem.save()

		return HttpResponseRedirect(reverse("admin_app:problem_detail", args=[problem_id,]))




	else:
		pass	