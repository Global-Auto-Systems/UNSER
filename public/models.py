from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group, User
from django.urls import reverse
from ministry.models import *
from django.core.validators import MinLengthValidator

class Service(models.Model):
	name = models.CharField(max_length=45, unique=True, verbose_name="Service Name")
	def __str__(self):
		return self.name

class Status(models.Model):
	name = models.CharField(max_length=45, unique=True, verbose_name="Application Status")
	def __str__(self):
		return self.name

class Classe(models.Model):
	name = models.CharField(max_length=45, unique=True,)
	def __str__(self):
		return self.name

class Report(models.Model):
	name = models.CharField(max_length=250, blank=True, null=True,)
	school = models.CharField(max_length=250, blank=True, null=True,)
	address = models.CharField(max_length=250, blank=True, null=True,)
	phone = models.CharField(max_length=13, validators=[MinLengthValidator(4)], blank=True, null=True,)
	email = models.CharField(max_length=30,blank=True, null=True,)
	case = models.TextField(blank=True, null=True,)
	covid = models.BooleanField(default=True,)
	to = models.ForeignKey(Group, blank=True, null=True, on_delete = models.SET_NULL)
	date = models.DateField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.name} {self.case}'

class ServiceProvider(models.Model):
	name = models.CharField(max_length=250, verbose_name="Service Provider Name")
	capacity = models.CharField(max_length=250, blank=True, null=True,)
	address = models.CharField(max_length=250, blank=True, null=True,)
	phone = models.CharField(max_length=13,blank=True, null=True,)
	email = models.CharField(max_length=30,blank=True, null=True,)
	description = models.TextField(blank=True, null=True,)
	service = models.ForeignKey(Service, on_delete = models.CASCADE)
	district = models.ForeignKey(District, blank=True, null=True, on_delete = models.SET_NULL)
	status = models.ForeignKey(Status, default=1, on_delete = models.SET_DEFAULT)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return self.name

	class Meta():
		unique_together=['service','email',]

class LockdownPackage(models.Model):
	subject = models.ManyToManyField(Subject,)
	topic = models.CharField(max_length = 200, blank=True, null=True,)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True, )
	home_class = models.ForeignKey(Classe, on_delete = models.CASCADE, verbose_name="Package Work Class")
	home_work = models.FileField(upload_to="lockdown_package")	
	def __str__(self):
		return f'{self.home_class} {self.subject} {self.topic}'

class DownloadResource(models.Model):
	topic = models.CharField(max_length = 200,)
	date_created = models.DateTimeField(default=timezone.now)
	date = models.DateField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True, )
	upload = models.FileField(upload_to="resources")	
	def __str__(self):
		return self.topic

class Communication(models.Model):
	topic = models.CharField(max_length = 200,)
	message = models.TextField(blank=True, null=True,)
	date_created = models.DateTimeField(default=timezone.now)
	date = models.DateField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True, )
	upload = models.FileField(upload_to="resources", blank=True, null=True,)	
	def __str__(self):
		return self.topic