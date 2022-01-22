from django.shortcuts import render, redirect
from ministry.models import *
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.views.generic import (
	ListView,
	DetailView,
	UpdateView,
	CreateView
	)
from django.db import IntegrityError
from django.db.models import Sum, Count

def home(request):
	schools = School.objects.all().order_by('name')
	context = {
	'title': 'Home',
	'schools':schools,
	}
	return render(request, 'public/home.html', context)

def schools(request, pk):
	item = District.objects.first()
	if request.GET.get('dist', None):
		dis_id=request.GET.get('dist', None)
		item = District.objects.get(pk=dis_id)
	level = Level.objects.get(pk=pk)
	schools = School.objects.filter(level=level, parish__district=item)
	records = District.objects.annotate(total_schools=Count('parish__school'))
	context = {
	'title': 'Schools',
	'head': 'in',
	'sub_title': 'District',
	'link': 'dist',
	'side_title': 'Districts',
	'schools':schools,
	'records':records,
	'level':level,
	'item':item,

	}
	return render(request, 'public/schools.html', context)

def university(request, pk):
	item = District.objects.first()
	if request.GET.get('dist', None):
		dis_id=request.GET.get('dist', None)
		item = District.objects.get(pk=dis_id)
	level = Level.objects.get(pk=pk)
	schools = School.objects.filter(level=level, parish__district=item)
	records = District.objects.annotate(total_schools=Count('parish__school'))
	context = {
	'title': 'Schools',
	'head': 'in',
	'sub_title': 'District',
	'link': 'dist',
	'side_title': 'Districts',
	'schools':schools,
	'records':records,
	'level':level,
	'item':item,

	}
	return render(request, 'public/schools.html', context)

def operation_status(request, pk):
	item = Schtype.objects.first()
	if request.GET.get('status', None):
		dis_id=request.GET.get('status', None)
		item = Schtype.objects.get(pk=dis_id)
	level = Level.objects.get(pk=pk)
	schools = School.objects.filter(level=level, operation_status=item)
	records = Schtype.objects.annotate(total_schools=Count('school'))
	context = {
	'title': 'Schools',
	'head': 'With Operation Status',
	'sub_title': 'Operation Status',
	'link': 'status',
	'side_title': 'Operation Status',
	'schools':schools,
	'records':records,
	'level':level,
	'item':item,
	}
	return render(request, 'public/schools.html', context)

def founder(request, pk):
	item = Ownership.objects.first()
	if request.GET.get('status', None):
		dis_id=request.GET.get('status', None)
		item = Ownership.objects.get(pk=dis_id)
	level = Level.objects.get(pk=pk)
	schools = School.objects.filter(level=level, founder=item)
	records = Ownership.objects.annotate(total_schools=Count('school'))
	context = {
	'title': 'Schools',
	'head': 'With Founding Body',
	'sub_title': 'Founding Body',
	'link': 'founder',
	'side_title': 'Founding Bodies',
	'schools':schools,
	'records':records,
	'level':level,
	'item':item,
	}
	return render(request, 'public/schools.html', context)

def funders(request, pk):
	item = Funder.objects.first()
	if request.GET.get('funder', None):
		dis_id=request.GET.get('funder', None)
		item = Funder.objects.get(pk=dis_id)
	level = Level.objects.get(pk=pk)
	schools = School.objects.filter(level=level, funder=item)
	records = Funder.objects.annotate(total_schools=Count('school'))
	context = {
	'title': 'Schools',
	'head': 'With Funding Source',
	'sub_title': 'Funders',
	'link': 'funder',
	'side_title': 'Funding Sources',
	'schools':schools,
	'records':records,
	'level':level,
	'item':item,
	}
	return render(request, 'public/schools.html', context)

def category(request, pk):
	item = Category.objects.first()
	if request.GET.get('category', None):
		dis_id=request.GET.get('category', None)
		item = Category.objects.get(pk=dis_id)
	level = Level.objects.get(pk=pk)
	schools = School.objects.filter(level=level, category=item)
	records = Category.objects.annotate(total_schools=Count('school'))
	context = {
	'title': 'Schools',
	'head': 'With Category',
	'sub_title': 'Category',
	'link': 'category',
	'side_title': 'Categories',
	'schools':schools,
	'records':records,
	'level':level,
	'item':item,
	}
	return render(request, 'public/schools.html', context)

def section(request, pk):
	item = Section.objects.first()
	if request.GET.get('section', None):
		dis_id=request.GET.get('section', None)
		item = Section.objects.get(pk=dis_id)
	level = Level.objects.get(pk=pk)
	schools = School.objects.filter(level=level, section=item)
	records = Section.objects.annotate(total_schools=Count('school'))
	context = {
	'title': 'Schools',
	'head': 'With Section',
	'sub_title': 'Section',
	'link': 'section',
	'side_title': 'Sections',
	'schools':schools,
	'records':records,
	'level':level,
	'item':item,
	}
	return render(request, 'public/schools.html', context)

def registration_status(request, pk):
	item = Regstatus.objects.first()
	if request.GET.get('status', None):
		dis_id=request.GET.get('status', None)
		item = Regstatus.objects.get(pk=dis_id)
	level = Level.objects.get(pk=pk)
	schools = School.objects.filter(level=level, regstatus=item)
	records = Regstatus.objects.annotate(total_schools=Count('school'))
	context = {
	'title': 'Schools',
	'head': 'With Registration Status',
	'sub_title': 'Registration Status',
	'link': 'status',
	'side_title': 'Statuses',
	'schools':schools,
	'records':records,
	'level':level,
	'item':item,
	}
	return render(request, 'public/schools.html', context)

def nearest_school(request, pk):
	item = DistanceToNearestSchool.objects.first()
	if request.GET.get('distance', None):
		dis_id=request.GET.get('distance', None)
		item = DistanceToNearestSchool.objects.get(pk=dis_id)
	level = Level.objects.get(pk=pk)
	schools = School.objects.filter(level=level, distance_to_nearest_school=item)
	records = DistanceToNearestSchool.objects.annotate(total_schools=Count('school'))
	context = {
	'title': 'Schools',
	'head': 'With Distance To Nearest School of',
	'sub_title': 'Nearest School',
	'link': 'distance',
	'side_title': 'Distance Range',
	'schools':schools,
	'records':records,
	'level':level,
	'item':item,
	}
	return render(request, 'public/schools.html', context)

def nearest_deo(request, pk):
	item = DistanceToDeoOffice.objects.first()
	if request.GET.get('distance', None):
		dis_id=request.GET.get('distance', None)
		item = DistanceToDeoOffice.objects.get(pk=dis_id)
	level = Level.objects.get(pk=pk)
	schools = School.objects.filter(level=level, distance_to_deo_office=item)
	records = DistanceToDeoOffice.objects.annotate(total_schools=Count('school'))
	context = {
	'title': 'Schools',
	'head': 'With Distance To Main Office of DEO/DIS/ESA of',
	'sub_title': 'Nearest DEO',
	'link': 'distance',
	'side_title': 'Distance Range',
	'schools':schools,
	'records':records,
	'level':level,
	'item':item,
	}
	return render(request, 'public/schools.html', context)

def rural_urban(request, pk):
	item = RuralUrban.objects.first()
	if request.GET.get('status', None):
		dis_id=request.GET.get('status', None)
		item = RuralUrban.objects.get(pk=dis_id)
	level = Level.objects.get(pk=pk)
	schools = School.objects.filter(level=level, rural_urban=item)
	records = RuralUrban.objects.annotate(total_schools=Count('school'))
	context = {
	'title': 'Schools',
	'head': 'With Status',
	'sub_title': 'Rural/Urban',
	'link': 'status',
	'side_title': 'Rural/Urban',
	'schools':schools,
	'records':records,
	'level':level,
	'item':item,
	}
	return render(request, 'public/schools.html', context)

def access(request, pk):
	item = Access.objects.first()
	if request.GET.get('access', None):
		dis_id=request.GET.get('access', None)
		item = Access.objects.get(pk=dis_id)
	level = Level.objects.get(pk=pk)
	schools = School.objects.filter(level=level, access=item)
	records = Access.objects.annotate(total_schools=Count('school'))
	context = {
	'title': 'Schools',
	'head': 'With Access Level',
	'sub_title': 'Access',
	'link': 'access',
	'side_title': 'Access',
	'schools':schools,
	'records':records,
	'level':level,
	'item':item,
	}
	return render(request, 'public/schools.html', context)

def school_levels(request, pk):
	schtype = Level.objects.first()
	school_list = School.objects.filter(level=pk).order_by('name')
	paginator = Paginator(school_list, 1000)
	page = request.GET.get('page')
	schools = paginator.get_page(page)
	context = {
	'title': 'Schools', 
	'schools': schools, 
	'schtype':schtype,

	}
	return render(request, 'public/schools.html', context)

def school(request, pk):
	school = School.objects.get(pk=pk)
	teachers = Teacher.objects.filter(school=school).order_by('-id')
	context = {
	'title': 'Schools', 
	'school': school,
	'teachers': teachers,

	}
	return render(request, 'public/school.html', context)

def teachers(request):
	teacher_list = District.objects.annotate(total_teachers = Count('district')).order_by('-total_teachers')
	paginator = Paginator(teacher_list, 1000)
	page = request.GET.get('page')
	teachers = paginator.get_page(page)
	context = {'title': 'Teachers', 'teachers': teachers}
	return render(request, 'public/teachers.html', context)

def deos(request):
	deo_list = Deo.objects.all().order_by('name')
	paginator = Paginator(deo_list, 1000)
	page = request.GET.get('page')
	deos = paginator.get_page(page)
	return render(request, 'public/DEOs.html', {'title': 'DEOs','deos': deos})

def service_providers(request):
	provider_list = ServiceProvider.objects.filter(status=2).order_by('name')
	paginator = Paginator(provider_list, 1000)
	page = request.GET.get('page')
	service_providers = paginator.get_page(page)
	context = {
	'title': 'Service Providers', 
	'service_providers': service_providers,

	}
	return render(request, 'public/service_providers.html', context)

def apply(request):
	if request.method == 'POST':
		apply_form = ApplyCreateForm(request.POST, request.FILES,)
		if apply_form.is_valid():
			try:
				apply_form.save()
				messages.success(request, f'Thank you! You have applied to be added as a service provider.')
				return HttpResponseRedirect(reverse('apply'))
			except Exception:
				messages.warning(request, f'Error! Your application did not complete!')		
	else:
		apply_form = ApplyCreateForm()

	context = {
	'title': 'Service Providers',
	'apply_form': apply_form,
	}
	return render(request, 'public/apply_form.html', context)

def report(request):
	if request.method == 'POST':
		form = ReportCreateForm(request.POST, request.FILES,)
		if form.is_valid():
			try:
				form.save()
				messages.success(request, f'Thank you! You have reported your case successifully.')
				return HttpResponseRedirect(reverse('report'))
			except Exception:
				messages.warning(request, f'Error! Your case is not reported, Try again!')		
	else:
		form = ReportCreateForm()

	context = {
	'title': 'Report',
	'form': form,
	'groups': Group.objects.filter(pk__lte=4),
	}
	return render(request, 'public/report.html', context)

def covid19(request):
	classes = Classe.objects.annotate(uploads=Count('lockdownpackage')).order_by('id')
	return render(request, 'public/covid19.html', {'title': 'COVID-19','classes': classes})

def covid19_downloads(request, pk):
	the_class = Classe.objects.get(pk=pk)
	uploads = LockdownPackage.objects.filter(home_class=the_class).order_by('-id')
	classes = Classe.objects.annotate(uploads=Count('lockdownpackage')).exclude(pk=pk).order_by('id')
	context = {
	'title': 'COVID-19',
	'classes': classes,
	'the_class': the_class,
	'uploads': uploads, 
	}
	return render(request, 'public/covid19_downloads.html', context)


def results(request):
	return render(request, 'public/results.html', {'title': 'UNEB Results'})

def uace_results(request):
	year = 2020
	if request.GET.get('year', None):
		year = request.GET.get('year', None)
	the_results = SchoolRankUACE.objects.filter(year=year).order_by('rank')[:500]
	context = {
		'title': 'UNEB Results',
		'results':the_results,
		'year':year,
	}
	return render(request, 'public/results_uace.html', context)

def uce_results(request):
	year = 2020
	if request.GET.get('year', None):
		year = request.GET.get('year', None)
	the_results = SchoolRankUCE.objects.filter(year=year).order_by('rank')[:500]

	context = {
		'title': 'UNEB Results',
		'head': 'UCE',
		'results':the_results,
		'year':year
	}
	return render(request, 'public/results_uce.html', context)

def ple_results(request):
	year = 2020
	if request.GET.get('year', None):
		year = request.GET.get('year', None)
	the_results = SchoolRankPLE.objects.filter(year=year).order_by('rank')[:500]
	context = {
		'title': 'UNEB Results',
		'head': 'PLE',
		'results':the_results,
		'year':year
	}
	return render(request, 'public/results_uce.html', context)

def marketing(request):
	return render(request, 'public/marketing.html', {'title': 'Marketing'})

def communication(request):
	context = {
		'title': 'Communication',
		'communications':Communication.objects.all().order_by('-id')[:500]
		}
	return render(request, 'public/communication.html', context)

def resources(request):
	context = {
		'title':'Resources',
		'resources':DownloadResource.objects.all().order_by('-id')[:500]
	}
	return render(request, 'public/resources.html', context)

def settings(request):
	return render(request, 'public/settings.html', {'title': 'Settings'})

def search_google(request):
	return render(request, 'public/search_google.html', {'title': 'Search'})

class SliderTemplate(TemplateView):
	template_name = 'public/slider.html'

class SliderMainTemplate(TemplateView):
	template_name = 'public/slider_main.html'
