from django.shortcuts import render,  redirect
from django.db.models.signals import post_save
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import *
from .models import *
from ministry.models import *
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
	ListView,
	DetailView,
	UpdateView,
	CreateView
	)

def login_success(request):
	usergroup = None
	if request.user.is_authenticated:
		usergroup = request.user.groups.values_list('id', flat=True).last()
	if usergroup == settings.MINISTRY_GROUP_ID:
		return redirect('ministry-home')
	if usergroup == settings.SCHOOL_GROUP_ID:
		return redirect('school-home')
	if usergroup == settings.PARTNER_GROUP_ID:
		return redirect('partners-home')
	if usergroup == settings.MARKETING_GROUP_ID:
		return redirect('serviceproviders-home')
	if usergroup == settings.POLICE_GROUP_ID:
		return redirect('police-home')
	else:
		return redirect('website-home')

@login_required
def updateprofile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
		if u_form.is_valid() and u_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Thank you! Your profile has been updated')

	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = UserProfileUpdateForm(instance=request.user.userprofile)

	context = {
	'u_form':u_form,
	'p_form':p_form,
	'title': 'Home'
	}
	return render(request, 'users/profile.html', context)

class ProfileListView(ListView):
	model = UserProfile
	context_object_name = 'profiles'
	ordering = ['-id']

def profile(request):
	context = {
	'title': 'Home'
	}
	return render(request, 'users/userprofile_detail.html', context)

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			group = Group.objects.get(pk=settings.PUBLIC_GROUP_ID)
			user.groups.add(group)
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'ministry/base.html', {'form': form, 'title': 'Register'})

def register_school(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			group = Group.objects.get(pk=settings.SCHOOL_GROUP_ID)
			user.groups.add(group)
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'ministry/base.html', {'form': form, 'title': 'Register'})