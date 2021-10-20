from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class AppUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=50, default="none")
	last_name = models.CharField(max_length=50, default="none")
	email = models.CharField(max_length=50, default="none")

	auth_code = models.CharField(max_length=50, default="none")
	request_code = models.CharField(max_length=50, default="none")

	ec_status = models.BooleanField(default=False)

	status = models.BooleanField(default=False)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.user.username



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



class Problem(models.Model):
	app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
	title = models.CharField(max_length=50, default="none")
	detail = models.CharField(max_length=100, default="none")
	video = models.FileField(upload_to='app_files/videos/', blank=True, default="default_files/default.mp4")

	category = models.CharField(max_length=50, default="none")
	tag1 = models.CharField(max_length=20, default="none")
	tag2 = models.CharField(max_length=20, default="none")
	tag3 = models.CharField(max_length=20, default="none")
	tag4 = models.CharField(max_length=20, default="none")
	tag5 = models.CharField(max_length=20, default="none")

	claps = models.ManyToManyField(Clap, through="ProblemClapConnector")
	buzzers = models.ManyToManyField(Buzzer, through="ProblemBuzzerConnector")

	status = models.BooleanField(default=False)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title



class Solution(models.Model):
	app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
	problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

	title = models.CharField(max_length=50, default="none")
	detail = models.CharField(max_length=100, default="none")

	claps = models.ManyToManyField(Clap, through="SolutionClapConnector")
	buzzers = models.ManyToManyField(Buzzer, through="SolutionBuzzerConnector")

	rating = models.IntegerField(default=0)

	video = models.FileField(upload_to='app_files/videos/', blank=True, default="default_files/default.mp4")

	status = models.BooleanField(default=False)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.problem.title






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

