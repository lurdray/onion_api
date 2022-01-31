from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from main.models import *

# Create your views here.





def ConfirmPaymentView(request):
	

	if request.method == "POST":
		username = request.POST.get("username")

		try:
			app_user = AppUser.objects.get(user__username=username)
			app_user.payment_status = True
			app_user.save()

			return HttpResponse("Payment confirmed, returning back to app.")

		except:
			return HttpResponse("Sorry there was an issue, returning back to app.")


		
	else:

		context = {
		}

		return render(request, "admin_app/confirm_payment.html", context)


def SignInView(request):

	if request.method == "POST":

		username = request.POST.get("username")
		password = request.POST.get("password")


		user = authenticate(username=username, password=password)

		if user:
			if user.is_active and user.is_superuser:
				login(request, user)
				return HttpResponseRedirect(reverse("admin_app:index"))


			else:
				context = {"msg": "Sorry, you are not at admin."}
				return render(request, "admin_app/sign_in.html", context)

		else:
			context = {"msg": "Sorry, invalid logins."}
			return render(request, "admin_app/sign_in.html", context)


				
	else:

		context = {}
		return render(request, "admin_app/sign_in.html", context)




def SignOutView(request):
	logout(request)

	return HttpResponseRedirect(reverse("admin_app:sign_in"))




def AllCategoriesView(request):
	categories = Category.objects.order_by("-pub_date")
	if request.method == "POST":

		name = request.POST.get("name")

		category = Category.objects.create(name=name)
		category.save()

		return HttpResponseRedirect(reverse("admin_app:all_categories"))

		

		
	else:
		context = {
		"categories": categories
		}

		return render(request, "admin_app/all_categories.html", context)




def CategoryDetailView(request, category_id):
	category = Category.objects.get(id=category_id)
	if request.method == "POST":
		new_name = request.POST.get("new_name")
		category.name = new_name
		category.save()

		return HttpResponseRedirect(reverse("admin_app:all_categories"))
		
	else:

		context = {
		"category": category
		}

		return render(request, "admin_app/category_detail.html", context)




def DeleteCategoryView(request, category_id):
	category = Category.objects.get(id=category_id)
	if request.method == "POST":
		category = Category.objects.get(id=category_id)
		category.delete()

		return HttpResponseRedirect(reverse("admin_app:all_categories"))

		
	else:
		context = {
		"category": category
		}

		return render(request, "admin_app/delete_category.html", context)
		

		


def IndexView(request):

	if request.method == "POST":
		pass

		
	else:

		try:
			user = User.objects.get(pk=request.user.id)
			if user.is_superuser:

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


			else:
				return HttpResponseRedirect(reverse("admin_app:sign_out"))

		except:
			return HttpResponseRedirect(reverse("admin_app:sign_out"))


def AllProblemsView(request):

	if request.method == "POST":
		pass

		
	else:

		problems = Problem.objects.all().order_by("-pub_date")

		context = {
		"problems": problems
		}

		return render(request, "admin_app/all_problems.html", context)




def ReportedVideosView(request):

	if request.method == "POST":
		pass

		
	else:

		problems = Problem.objects.all().order_by("-pub_date")
		solutions = Solution.objects.all().order_by("-pub_date")

		reported_p_videos = []
		reported_s_videos = []

		for item in problems:
			if item.report_count > 0:
				reported_p_videos.append(item)

		for item in solutions:
			if item.report_count > 0:
				reported_s_videos.append(item)


		

		context = {
		"reported_p_videos": reported_p_videos,
		"reported_s_videos": reported_s_videos

		}

		return render(request, "admin_app/reported_videos.html", context)


def ReportPDetailView(request, problem_id):

	if request.method == "POST":
		pass

		
	else:
		problem = Problem.objects.get(id=problem_id)
		reports = problem.reports.all()

		context = {
			"problem": problem, 
			"reports": reports,
			}

		return render(request, "admin_app/report_p_detail.html", context)



def ReportSDetailView(request, solution_id):

	if request.method == "POST":
		pass

		
	else:
		solution = Solution.objects.get(id=solution_id)
		reports = solution.reports.all()

		context = {
			"solution": solution, 
			"reports": reports,
			}

		return render(request, "admin_app/report_s_detail.html", context)






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
		
		nt = Notification.objects.create(app_user=solution.app_user, detail="Your solution video for (%s) have been approved!" % (solution.title), object_id="None")
		nt.save()

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
		
		nt = Notification.objects.create(app_user=problem.app_user, detail="Your problem video (%s) has been approved!" % (problem.title), object_id="None")
		nt.save()
				

		app_users = AppUser.objects.all()
		for item in app_users:
			if item.interest == problem.category:
				nt2 = Notification.objects.create(app_user=item, detail="New Problem Alert! (%s)" % (problem.title), object_id="None")
				nt2.save()

		return HttpResponseRedirect(reverse("admin_app:problem_detail", args=[problem_id,]))




	else:
		pass	