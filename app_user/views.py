from django.contrib import messages
from django.shortcuts import (HttpResponse, HttpResponseRedirect, get_object_or_404, redirect, render)
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from django.utils import timezone
import datetime

from main.models import *
import requests
from app_user.forms import *

import random
import string


from django.core.mail import send_mail
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.db.models import Q




def RaySendMail(subject, message, to_email, code=None):

    try:
        context = {"subject": subject, "message": message, "code": code}
        html_message = render_to_string('main/message.html', context)
        message = strip_tags(message)
    
        send_mail(
            subject,
            message,
            'hello@helloonions.com',
            [to_email,],
            html_message=html_message,
            fail_silently=False,
        )

    except:
        pass




def ray_randomiser(length=12):
	landd = string.ascii_letters + string.digits
	return ''.join((random.choice(landd) for i in range(length)))


def SignInView(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)

				app_user = AppUser.objects.get(user__pk=request.user.id)

				print("11111111111111111111111111111111")
				messages.success(request, "Welcome Onboard")
				return HttpResponseRedirect(reverse("app_user:index"))


			else:
				print("22222222222222222222222222222222")
				messages.warning(request, "Sorry, Invalid Login Details")
				return HttpResponseRedirect(reverse("app_user:sign_in"))

		else:
			print("33333333333333333333333333333333333333")
			messages.warning(request, "Sorry, Invalid Login Details")
			return HttpResponseRedirect(reverse("app_user:sign_in"))

	else:
		context = {}
		return render(request, "app_user/sign_in.html", context )




def SignUpView(request):
	if request.method == "POST":

		form = UserForm(request.POST or None, request.FILES or None)
		email = request.POST.get("username")
		password1 = request.POST.get("password1")
		password2 = request.POST.get("password2")

		first_name = request.POST.get("first_name")
		last_name = request.POST.get("last_name")
		interest = request.POST.get("interest")

		request.session.create()
		auth_code = request.session.session_key

		app_users = AppUser.objects.filter(user__username=request.POST.get("username"))

		if request.POST.get("password2") != request.POST.get("password1"):
			messages.warning(request, "Make sure both passwords match")
			print("passwords didn't match")
			return HttpResponseRedirect(reverse("app_user:sign_up"))

		elif len(app_users) > 0:
			messages.warning(request, "Email Address already taken, try another one!")
			print("email address already taken")
			return HttpResponseRedirect(reverse("app_user:sign_up"))
			
		else:
			user = form.save()
			user.set_password(request.POST.get("password1"))
			user.save()

			app_user = AppUser.objects.create(user=user, first_name=first_name, last_name=last_name,
				interest=interest, email=user.username, auth_code=auth_code)
				
			request_code = ray_randomiser()
			app_user.request_code = request_code
			app_user.save()

			RaySendMail("Authentication", "Welcome to Onions, Please use the authentication code below to complete your sign up!", app_user.user.username, code=request_code)

			nt = Notification.objects.create(app_user=app_user, detail="Welcome to ONIONS", object_id="None")
			nt.save()

			if user:
				if user.is_active:
					login(request, user)

					app_user = AppUser.objects.get(user__pk=request.user.id)
					return HttpResponseRedirect(reverse("app_user:email_verify"))


	else:
		categories = Category.objects.all().order_by("-pub_date")
		form = UserForm()

		context = {"form": form, "categories": categories}
		return render(request, "app_user/sign_up.html", context )




def EmailVerifyView(request):

	app_user = AppUser.objects.get(user__pk=request.user.id)
	if request.method == "POST":
		auth_code = request.POST.get("auth_code")
		if auth_code == app_user.request_code:
			return HttpResponseRedirect(reverse("app_user:index"))

		else:
			msg = "Sorry, Invalid Auth Code."
			
			context = {"app_user": app_user, "msg": msg}
			return render(request, "app_user/email_verify.html", context)
			



	else:
		timelines = requests.post("https://helloonions.com/get-timeline/")
		timelines = timelines.json()

		context = {"app_user": app_user, "timelines": timelines}
		return render(request, "app_user/email_verify.html", context)




def SignOutView(request):
	app_user = AppUser.objects.get(user__pk=request.user.id)
	if request.method == "POST":
		pass


	else:
		timeline = []

		context = {"app_user": app_user, "timeline": timeline}
		return render(request, "app_user/timeline.html", context)






def IndexView(request):
	#needed objects
	try:
		app_user = AppUser.objects.get(user__pk=request.user.id)

	except:
		app_user = None

	categories = Category.objects.all().order_by('-pub_date')


	#app_user = None
	if request.method == "POST":
		pass


	else:
		problems = Problem.objects.filter(status=True).order_by('-pub_date')
		solutions = Solution.objects.filter(status=True).order_by('-pub_date')
		app_users = AppUser.objects.all()
		app_user_count = app_users.count()

		context = {"app_user": app_user, "categories": categories,
		 "problems": problems, "solutions": solutions, "app_users": app_users, "app_user_count": app_user_count}
		return render(request, "app_user/index.html", context)




def ProfileView(request):
	app_user = AppUser.objects.get(user__pk=request.user.id)
	categories = Category.objects.all().order_by('-pub_date')
	if request.method == "POST":
		pass


	else:

		context = {"app_user": app_user, "categories": categories}
		return render(request, "app_user/profile.html", context)




def TimelineView(request):
	app_user = AppUser.objects.get(user__pk=request.user.id)
	categories = Category.objects.all().order_by('-pub_date')
	if request.method == "POST":
		pass


	else:
		timeline = []

		context = {"app_user": app_user, "timeline": timeline, "categories": categories}
		return render(request, "app_user/timeline.html", context)




def AddProblemView(request):
	app_user = AppUser.objects.get(user__pk=request.user.id)
	if request.method == "POST":
		
		title = request.POST.get("title")
		detail = request.POST.get("detail")
		category = request.POST.get("category")
		tag = request.POST.get("tag")
		duration = request.POST.get("duration")

		today = timezone.now().date()
		nextD = today + datetime.timedelta(days=int(duration))

		video = request.FILES["video"]
		cover_image = request.FILES["cover_image"]

		

		problem = Problem.objects.create(app_user=app_user, auth_code=app_user.auth_code,
			app_user_name1=app_user.first_name, app_user_name2=app_user.last_name,
			profile_photo=app_user.profile_photo, title=title, detail=detail,
			category=category)

		category = Category.objects.create(name=category, creator=app_user.first_name)
		category.save()

		problem.video = video
		problem.cover_image = cover_image
		problem.app_user = app_user
		problem.switch_date = nextD
		problem.tag1 = tag
		problem.save()



		msg = "Congratulations! Video Uploaded. Kindly wait for approval."
		context = {"app_user": app_user, "msg": msg}
		return render(request, "app_user/notify.html", context)


	else:
		pass





def ProblemDetailView(request, problem_id):
	categories = Category.objects.all().order_by('-pub_date')
	try:
		app_user = AppUser.objects.get(user__pk=request.user.id)

	except:
		app_user = None
		
	if request.method == "POST":

		video = request.FILES["video"]
		
		problem = Problem.objects.get(id=problem_id)
		solution = Solution.objects.create(app_user=app_user, auth_code=app_user.auth_code, app_user_name1=app_user.first_name, app_user_name2=app_user.last_name, profile_photo=app_user.profile_photo, problem=problem, title=problem.title, detail=problem.detail)
		solution.video = video
		solution.save()

		msg = "Congratulations! Video Uploaded. Kindly wait for approval."
		context = {"app_user": app_user, "msg": msg, "categories": categories}
		return render(request, "app_user/notify.html", context)




	else:
		problem = Problem.objects.get(id=problem_id)
		solutions = Solution.objects.filter(problem=problem).order_by('-pub_date')

		context = {"app_user": app_user, "problem": problem, "solutions": solutions, "categories": categories}
		return render(request, "app_user/problem_detail.html", context)




def ProfileView(request):
	app_user = AppUser.objects.get(user__pk=request.user.id)
	categories = Category.objects.all().order_by('-pub_date')
	if request.method == "POST":
		first_name = request.POST.get("first_name")
		last_name = request.POST.get("last_name")
		interest = request.POST.get("interest")


		cover_image = request.FILES["cover_image"]
		profile_photo = request.FILES["profile_photo"]

		app_user.first_name = first_name
		app_user.last_name = last_name
		app_user.interest = interest
		app_user.cover_image = cover_image
		app_user.profile_photo = profile_photo
		app_user.save()


		msg = "Profile data uploaded!"
		context = {"app_user": app_user, "msg": msg, "categories": categories}
		return render(request, "app_user/notify.html", context)





	else:
		problems = Problem.objects.filter(app_user=app_user).order_by('-pub_date')
		solutions = Solution.objects.filter(app_user=app_user).order_by('-pub_date')

		problem_count = problems.count()
		solution_count = solutions.count()

		interests = Category.objects.all().order_by('-pub_date')


		context = {"app_user": app_user, "problems": problems, "solutions": solutions,
		"problem_count": problem_count, "solution_count": solution_count, "interests": interests, "categories": categories}
		return render(request, "app_user/profile.html", context)




def NotificationsView(request):
	app_user = AppUser.objects.get(user__pk=request.user.id)
	categories = Category.objects.all().order_by('-pub_date')
	if request.method == "POST":
		pass


	else:
		notifications = Notification.objects.filter(app_user=app_user).order_by('-pub_date')

		context = {"app_user": app_user, "notifications": notifications, "categories": categories}
		return render(request, "app_user/notifications.html", context)




def ClapSolutionView(request, solution_id):
	app_user = AppUser.objects.get(user__pk=request.user.id)
	categories = Category.objects.all().order_by('-pub_date')
	if request.method == "POST":

		solution = Solution.objects.get(id=solution_id)

		hand_status = False
		for clap in solution.claps.all():
			if clap.app_user.id == app_user.id:
				hand_status = True

		if hand_status == True:
			msg = "Sorry, you already clapped for this solutions!"
			context = {"app_user": app_user, "msg": msg}
			return render(request, "app_user/notify.html", context)


		else:
			clap = Clap.objects.create(app_user=app_user)

			sc = SolutionClapConnector(solution=solution, clap=clap)
			sc.save()

			solution.clap_count = solution.claps.count()
			solution.save()

			msg = "Congratulations, you just clapped for a solutions!"
			context = {"app_user": app_user, "msg": msg, "categories": categories}
			return render(request, "app_user/notify.html", context)


	else:
		pass





def BuzzSolutionView(request, solution_id):
	app_user = AppUser.objects.get(user__pk=request.user.id)
	categories = Category.objects.all().order_by('-pub_date')
	if request.method == "POST":

		solution = Solution.objects.get(id=solution_id)

		hand_status = False
		for buzz in solution.buzzers.all():
			if buzz.app_user.id == app_user.id:
				hand_status = True
	
		if hand_status == True:
			msg = "Sorry, you already buzzed this solutions!"
			context = {"app_user": app_user, "msg": msg}
			return render(request, "app_user/notify.html", context)


		else:
			buzzer = Buzzer.objects.create(app_user=app_user)

			sb = SolutionBuzzerConnector(solution=solution, buzzer=buzzer)
			sb.save()

			solution.buzzer_count = solution.buzzers.count()
			solution.save()

			msg = "Good one, you just buzzed solution!"
			context = {"app_user": app_user, "msg": msg, "categories": categories}
			return render(request, "app_user/notify.html", context)


	else:
		pass



def NotifyView(request, msg):
	app_user = AppUser.objects.get(user__pk=request.user.id)
	if request.method == "POST":
		pass



	else:

		context = {"app_user": app_user, "msg": msg}
		return render(request, "app_user/notify.html", context)

