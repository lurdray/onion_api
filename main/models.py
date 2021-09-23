from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class AppUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	full_name = models.CharField(max_length=120)
	email = models.CharField(max_length=120)

	status = models.BooleanField(default=False)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.user.username



class Problem(models.Model):
	app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
	title = models.CharField(max_length=50, default="none")
	detail = models.CharField(max_length=500, default="none")
	video = models.FileField(upload_to='app_files/videos/', blank=True, default="default_files/default.mp4")

	status = models.BooleanField(default=False)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title



class Solution(models.Model):
	app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
	problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

	title = models.CharField(max_length=50, default="none")
	detail = models.CharField(max_length=500, default="none")

	video = models.FileField(upload_to='app_files/videos/', blank=True, default="default_files/default.mp4")

	status = models.BooleanField(default=False)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.problem.title
