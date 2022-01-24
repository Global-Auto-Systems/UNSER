from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ministry.models import * 
from school.models import *

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	photo = models.ImageField(default='user_photos/default.png', upload_to='user_photos', blank=True, null=True,)
	address = models.CharField(max_length=200, blank=True, null=True)
	phone = models.CharField(max_length=200, blank=True, null=True)
	updated = models.DateTimeField(auto_now=True)
	def __str__(self):
		return f'{self.user.first_name} {self.user.last_name}'

class SchoolProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	school = models.OneToOneField(School, on_delete = models.CASCADE)
	group = models.IntegerField(default=settings.SCHOOL_GROUP_ID)

	def __str__(self):
		return f'{self.school.name}`s Profile'

class TeacherProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)
	group = models.IntegerField(default=settings.TEACHER_GROUP_ID)

	def __str__(self):
		return f'{self.teacher.name}`s Profile'

class DeoProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	deo = models.OneToOneField(Deo, on_delete=models.CASCADE)
	group = models.IntegerField(default=settings.DEO_GROUP_ID)

	def __str__(self):
		return f'{self.deo.name}`s Profile'

