from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import random
import string


class Category(models.Model):
	name =  models.CharField(max_length=50, default="none")
	creator = models.CharField(max_length=50, default="Admin")

	status = models.BooleanField(default=False)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.name

class AppUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	
	profile_photo = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="default_files/onion_pp.jpg")
	cover_image = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="default_files/default_image.jpg")
	
	first_name = models.CharField(max_length=50, default="none")
	last_name = models.CharField(max_length=50, default="none")

	interest = models.CharField(max_length=50, default="none")

	email = models.CharField(max_length=50, default="none")

	auth_code = models.CharField(max_length=50, default="none")
	request_code = models.CharField(max_length=50, default="none")

	payment_status = models.BooleanField(default=False)

	ec_status = models.BooleanField(default=False)

	status = models.BooleanField(default=False)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.user.username


class Notification(models.Model):
	app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
	detail =  models.CharField(max_length=50, default="none")
	object_id = models.CharField(max_length=50, default="none")

	status = models.BooleanField(default=False)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.detail

class Report(models.Model):
	app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

	reason =  models.CharField(max_length=50, default="none")
	status = models.BooleanField(default=True)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.app_user.first_name


class View(models.Model):
	app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

	status = models.BooleanField(default=True)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.app_user.first_name


class Clap(models.Model):
	app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

	status = models.BooleanField(default=True)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.app_user.first_name


class Buzzer(models.Model):
	app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

	status = models.BooleanField(default=True)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.app_user.first_name


class Comment(models.Model):
	app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=50, default="none")
	last_name = models.CharField(max_length=50, default="none")
	profile_photo = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="default_files/default_face.png")
	comment = models.CharField(max_length=200, default="none")

	status = models.BooleanField(default=True)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.app_user.first_name


class Problem(models.Model):
	app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
	auth_code = models.CharField(max_length=50, default="none")
	app_user_name1 = models.CharField(max_length=50, default="none")
	app_user_name2 = models.CharField(max_length=50, default="none")
	profile_photo = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="default_files/default_face.png")
	title = models.CharField(max_length=50, default="none")
	detail = models.CharField(max_length=100, default="none")
	cover_image = models.FileField(upload_to='app_files/cover_images/', blank=True, default="default_files/cover_imm.png")
	video = models.FileField(upload_to='app_files/videos/', blank=True, default="default_files/default.mp4")

	category = models.CharField(max_length=50, default="none")
	switch_date = models.DateTimeField(default=timezone.now)
	
	tag1 = models.CharField(max_length=20, default="none")
	tag2 = models.CharField(max_length=20, default="none")
	tag3 = models.CharField(max_length=20, default="none")
	tag4 = models.CharField(max_length=20, default="none")
	tag5 = models.CharField(max_length=20, default="none")

	views = models.ManyToManyField(View, through="ProblemViewConnector")
	view_count = models.IntegerField(default=0)

	claps = models.ManyToManyField(Clap, through="ProblemClapConnector")
	buzzers = models.ManyToManyField(Buzzer, through="ProblemBuzzerConnector")
	comments = models.ManyToManyField(Comment, through="ProblemCommentConnector")
	
	clap_count = models.IntegerField(default=0)
	buzzer_count = models.IntegerField(default=0)
	comment_count = models.IntegerField(default=0)

	#report shit
	reports = models.ManyToManyField(Report, through="ProblemReportConnector")
	report_count = models.IntegerField(default=0)

	rating = models.IntegerField(default=0)

	status = models.BooleanField(default=False)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title
		


class Solution(models.Model):
	app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
	auth_code = models.CharField(max_length=50, default="none")
	app_user_name1 = models.CharField(max_length=50, default="none")
	app_user_name2 = models.CharField(max_length=50, default="none")
	profile_photo = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="default_files/default_face.png")
	problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

	title = models.CharField(max_length=50, default="none")
	detail = models.CharField(max_length=100, default="none")

	views = models.ManyToManyField(View, through="SolutionViewConnector")
	view_count = models.IntegerField(default=0)

	claps = models.ManyToManyField(Clap, through="SolutionClapConnector")
	buzzers = models.ManyToManyField(Buzzer, through="SolutionBuzzerConnector")
	comments = models.ManyToManyField(Comment, through="SolutionCommentConnector")
	
	clap_count = models.IntegerField(default=0)
	buzzer_count = models.IntegerField(default=0)
	comment_count = models.IntegerField(default=0)

	reports = models.ManyToManyField(Report, through="SolutionReportConnector")
	report_count = models.IntegerField(default=0)

	rating = models.IntegerField(default=0)


	video = models.FileField(upload_to='app_files/videos/', blank=True, default="default_files/default.mp4")

	status = models.BooleanField(default=False)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title
		




class ProblemReportConnector(models.Model):
	problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
	report = models.ForeignKey(Report, on_delete=models.CASCADE)
	pub_date = models.DateTimeField(default=timezone.now)

class SolutionReportConnector(models.Model):
	solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
	report = models.ForeignKey(Report, on_delete=models.CASCADE)
	pub_date = models.DateTimeField(default=timezone.now)

class ProblemCommentConnector(models.Model):
	problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
	pub_date = models.DateTimeField(default=timezone.now)
	

class SolutionCommentConnector(models.Model):
	solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
	pub_date = models.DateTimeField(default=timezone.now)


class ProblemClapConnector(models.Model):
	problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
	clap = models.ForeignKey(Clap, on_delete=models.CASCADE)
	pub_date = models.DateTimeField(default=timezone.now)



class ProblemBuzzerConnector(models.Model):
	problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
	buzzer = models.ForeignKey(Buzzer, on_delete=models.CASCADE)
	pub_date = models.DateTimeField(default=timezone.now)



class SolutionClapConnector(models.Model):
	solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
	clap = models.ForeignKey(Clap, on_delete=models.CASCADE)
	pub_date = models.DateTimeField(default=timezone.now)



class SolutionBuzzerConnector(models.Model):
	solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
	buzzer = models.ForeignKey(Buzzer, on_delete=models.CASCADE)
	pub_date = models.DateTimeField(default=timezone.now)



class ProblemViewConnector(models.Model):
	problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
	view = models.ForeignKey(View, on_delete=models.CASCADE)
	pub_date = models.DateTimeField(default=timezone.now)


class SolutionViewConnector(models.Model):
	solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
	view = models.ForeignKey(View, on_delete=models.CASCADE)
	pub_date = models.DateTimeField(default=timezone.now)
