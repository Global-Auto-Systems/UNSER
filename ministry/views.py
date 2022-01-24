from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect
from django.views.generic import (
	ListView,
	DetailView,
	UpdateView,
	FormView,
	CreateView
	)

from .models import *
from .forms import *
from school.forms import *
from school.models import *
from django.http import JsonResponse
from django.db import IntegrityError
from django.db.models import Sum, Count, Q


# class HomeView(DetailView):
# 	model = School
# 	template_name = "ministry/home.html"
# 	def get_context_data(self, **kwargs):
# 		context = super(HomeView, self).get_context_data(**kwargs)
# 		context['all_schools'] = School.objects.all().order_by('-id')
# 		all_regs = School.objects.values("region").annotate(Count("id"))
# 		context['all_resources'] = Resource.objects.all().order_by('-id')
# 		context['teachers'] = Teacher.objects.all().order_by('-id')[:10]
# 		context['deos'] = Deo.objects.all().order_by('-id')
# 		context['teacher_transfers'] = TransferTeacher.objects.all().order_by('-id')
# 		context['deo_transfers'] = TransferDeo.objects.all().order_by('-id')
# 		context['allocated_resources'] = AllocateResource.objects.all().order_by('-id')
		# return context

# School related views..................................................................................
# School related views..................................................................................

class SchoolListView(ListView):
	model = School
	def get_context_data(self, **kwargs):
		context = super(SchoolListView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		schools = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["schools"] = schools.get_page(page)
		context["title"] = "Schools"
		return context

class SchoolDetailView(DetailView):
	model = School
	def get_context_data(self, **kwargs):
		context = super(SchoolDetailView, self).get_context_data(**kwargs)
		context["title"] = "Schools"
		return context

class SchoolCreateView(LoginRequiredMixin, CreateView):
	model = School
	template_name = "ministry/school_form.html"
	form_class = SchoolCreateForm
	def get_context_data(self, **kwargs):
		context = super(SchoolCreateView, self).get_context_data(**kwargs)
		context["title"] = "Schools"
		context["parishes"] = Parish.objects.all()
		context["regstatuses"] = Regstatus.objects.all()
		context["schtypes"] = Schtype.objects.all()
		context["founders"] = Ownership.objects.all()
		context["funders"] = Funder.objects.all()
		context["accesses"] = Access.objects.all()
		context["rural_urban"] = RuralUrban.objects.all()
		context["categories"] = Category.objects.all()
		context["sections"] = Section.objects.all()
		context["levels"] = Level.objects.all()
		context["classes"] = Class.objects.all()
		context["dns"] = DistanceToNearestSchool.objects.all()
		context["ddo"] = DistanceToDeoOffice.objects.all()
		return context

	def form_valid(self, form):
		form = SchoolCreateForm(self.request.POST, self.request.FILES)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('name')
				messages.success(self.request, f'Thank you! You have added {name}')
			except IntegrityError:
				name = form.cleaned_data.get('name')
				messages.warning(self.request, f'ERROR! Some thing went wrong. Try again')
			return redirect('new-school')

class SchoolUpdateView(LoginRequiredMixin, UpdateView):
	model = School
	template_name = "ministry/school_form.html"
	form_class = SchoolCreateForm
	def get_context_data(self, **kwargs):
		context = super(SchoolUpdateView, self).get_context_data(**kwargs)
		context["title"] = "Schools"
		context["parishes"] = Parish.objects.all()
		context["regstatuses"] = Regstatus.objects.all()
		context["schtypes"] = Schtype.objects.all()
		context["founders"] = Ownership.objects.all()
		context["funders"] = Funder.objects.all()
		context["accesses"] = Access.objects.all()
		context["rural_urban"] = RuralUrban.objects.all()
		context["categories"] = Category.objects.all()
		context["sections"] = Section.objects.all()
		context["levels"] = Level.objects.all()
		context["classes"] = Class.objects.all()
		context["dns"] = DistanceToNearestSchool.objects.all()
		context["ddo"] = DistanceToDeoOffice.objects.all()
		return context

	def form_valid(self, form):
		school = School.objects.get(pk=self.object.id)
		form = SchoolCreateForm(self.request.POST, self.request.FILES, instance=school)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('name')
				messages.success(self.request, f'Thank you! You have updated {name}')
			except IntegrityError:
				name = form.cleaned_data.get('name')
				messages.warning(self.request, f'ERROR! Some thing went wrong. Try again')
			return redirect('new-school')
		return redirect('new-school')


# Teacher related views..................................................................................
# Teacher related views..................................................................................

class TeacherCreateView(LoginRequiredMixin, CreateView):
	model = Teacher
	form_class = TeacherCreateForm
	def get_context_data(self, **kwargs):
		context = super(TeacherCreateView, self).get_context_data(**kwargs)
		context["genders"] = Gender.objects.all()
		context["educations"] = TeacherEducation.objects.all()
		context["professions"] = TeacherProfession.objects.all()
		context["responsibilities"] = TeacherResponsibility.objects.all()
		context["salary_scales"] = TeacherSalaryScale.objects.all()
		context["trainings"] = TeacherTraining.objects.all()
		context["districts"] = District.objects.all()
		context["subjects"] = Subject.objects.all()
		context["title"] = "Teachers"
		return context

	def form_valid(self, form):
		form = TeacherCreateForm(self.request.POST, self.request.FILES)
		if form.is_valid():
			form.instance.user = self.request.user
			form.instance.school = self.request.user.schoolprofile.school
			try:
				form.save()
				name = form.cleaned_data.get('surname')
				first_name = form.cleaned_data.get('first_name')
				messages.success(self.request, f'Thank you! You have added {name} {first_name}')
			except IntegrityError:
				messages.warning(self.request, f'ERROR! Some thing went wrong. Try again')
			return redirect('new-teacher')

class TeacherUpdateView(LoginRequiredMixin, UpdateView):
	form_class = TeacherCreateForm
	model = Teacher
	def get_context_data(self, **kwargs):
		context = super(TeacherUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		teachers = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["teachers"] = teachers.get_page(page)
		context["title"] = "Teachers"
		return context

	def form_valid(self, form):
		teacher = Teacher.objects.get(pk=self.object.id)
		form = TeacherCreateForm(self.request.POST, self.request.FILES, instance=teacher)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('name')
				messages.success(self.request, f'Thank you! You have updated {name}')
			except IntegrityError:
				name = form.cleaned_data.get('name')
				messages.warning(self.request, f'ERROR! Some thing went wrong. Try again')
			return redirect('new-teacher')

class TeacherListView(ListView):
	model = Teacher
	def get_context_data(self, **kwargs):
		context = super(TeacherListView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		teachers = Paginator(self.model.objects.filter(school=self.request.user.schoolprofile.school).order_by('-id'), 1000)
		context["teachers"] = teachers.get_page(page)
		context["title"] = "Teachers"
		return context

class TeacherDetailView(DetailView):
	model = Teacher
	def get_context_data(self, **kwargs):
		context = super(TeacherDetailView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		teachers = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["teachers"] = teachers.get_page(page)
		context["title"] = "Teachers"
		return context

class TeacherTransferListView(ListView):
	model = TransferTeacher
	def get_context_data(self, **kwargs):
		context = super(TeacherTransferListView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		teachers = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["teacher_transfers"] = teachers.get_page(page)
		context["title"] = "Teachers"
		return context

class TransferTeacherCreateView(LoginRequiredMixin, CreateView):
	model = TransferTeacher
	form_class = TeacherTransferForm
	def get_context_data(self, **kwargs):
		context = super(TransferTeacherCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		teachers = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["transfers"] = teachers.get_page(page)
		context["title"] = "Teachers"
		return context

	def form_valid(self, form):
		form = TeacherTransferForm(self.request.POST, self.request.FILES,)
		if form.is_valid():
			form.instance.user = self.request.user
			form.save(commit=False)
			teacher = form.cleaned_data.get('teacher')
			form.instance.school_from = teacher.school
			try:
				form.save()
				teacher = form.cleaned_data.get('teacher')
				messages.success(self.request, f'Thank you! The Transfer of {teacher} was successful')
			except IntegrityError:
				messages.warning(self.request, f'ERROR! Some thing went wrong. Try again')
			return redirect('transfer-teacher')

class TransferTeacherUpdateView(LoginRequiredMixin, UpdateView):
	model = TransferTeacher
	form_class = TeacherTransferForm
	def get_context_data(self, **kwargs):
		context = super(TransferTeacherUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		transfers = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["transfers"] = transfers.get_page(page)
		context["title"] = "Teachers"
		return context

	def form_valid(self, form):
		transfer = TransferTeacher.objects.get(pk=self.object.id)
		form = TeacherTransferForm(self.request.POST, self.request.FILES, instance=transfer)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('teacher')
				messages.success(self.request, f'Thank you! You have updated {name}`s transfer')
			except IntegrityError:
				name = form.cleaned_data.get('teacher')
				messages.warning(self.request, f'ERROR! Some thing went wrong. Try again')
			return redirect('transfer-teacher')


class DesignationCreateView(LoginRequiredMixin, CreateView):
	model = TeacherResponsibility
	fields =['responsibility']
	def get_context_data(self, **kwargs):
		context = super(DesignationCreateView, self).get_context_data(**kwargs)
		context["des"] = self.model.objects.all().order_by('-id')
		return context

	def form_valid(self, form):
		form.save()
		return redirect('responsibility')

class DesignationUpdateView(LoginRequiredMixin, UpdateView):
	model = TeacherResponsibility
	fields =['des_type']
	def get_context_data(self, **kwargs):
		context = super(DesignationUpdateView, self).get_context_data(**kwargs)
		context["des"] = self.model.objects.all().order_by('-id')
		return context

	def form_valid(self, form):
		form.save()
		return redirect('designation')

# Deo related views..................................................................................
# Deo related views..................................................................................

class DeoCreateView(LoginRequiredMixin, CreateView):
	model = Deo
	fields =['name','email','status','gender','district','region','photo']
	def get_context_data(self, **kwargs):
		context = super(DeoCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		deos = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["deos"] = deos.get_page(page)
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('new-deo')

class DeoUpdateView(LoginRequiredMixin, UpdateView):
	model = Deo
	fields =['name','email','status','gender','district','region','photo']
	def get_context_data(self, **kwargs):
		context = super(DeoUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		deos = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["deos"] = deos.get_page(page)
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('new-deo')

class DeoListView(ListView):
	model = Deo
	context_object_name = 'deos'
	ordering = ['-id']

class DeoDetailView(DetailView):
	model = Deo
	def get_context_data(self, **kwargs):
		context = super(DeoDetailView, self).get_context_data(**kwargs)
		context['deotransfers'] = TransferDeo.objects.filter(deo=self.object)
		return context

class TransferDeoCreateView(LoginRequiredMixin, CreateView):
	model = TransferDeo
	fields =['deo','district','date_transfered','date_valid']
	def get_context_data(self, **kwargs):
		context = super(TransferDeoCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		deotransfers = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["deotransfers"] = deotransfers.get_page(page)
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('transfer-deo')

class TransferDeoUpdateView(LoginRequiredMixin, UpdateView):
	model = TransferDeo
	fields =['deo','district','date_transfered','date_valid']
	def get_context_data(self, **kwargs):
		context = super(TransferDeoUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		deotransfers = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["deotransfers"] = deotransfers.get_page(page)
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('transfer-deo')

# Fac related views..................................................................................
# Fac related views..................................................................................

class FacilityCreateView(LoginRequiredMixin, CreateView):
	model = Facility
	fields =['facility_type','description','quantity','status','photo']
	template_name = "ministry/facility_form.html"
	def get_context_data(self, **kwargs):
		context = super(FacilityCreateView, self).get_context_data(**kwargs)
		context["facilities"] = self.model.objects.all().order_by('-id')
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		# form.instance.school = self.request.session.get['sch_id']
		form.save()
		return HttpResponseRedirect("")
		# return redirect('new-facility')

# School settings related views..................................................................................
# School settings views..................................................................................

class OwnershipCreateView(LoginRequiredMixin, CreateView):
	model = Ownership
	fields =['own_type']
	def get_context_data(self, **kwargs):
		context = super(OwnershipCreateView, self).get_context_data(**kwargs)
		context["own_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('ownership')

class OwnershipUpdateView(LoginRequiredMixin, UpdateView):
	model = Ownership
	fields =['own_type']
	def get_context_data(self, **kwargs):
		context = super(OwnershipUpdateView, self).get_context_data(**kwargs)
		context["own_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('ownership')

class SectionCreateView(LoginRequiredMixin, CreateView):
	model = Section
	fields =['sec_type']
	def get_context_data(self, **kwargs):
		context = super(SectionCreateView, self).get_context_data(**kwargs)
		context["sec_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('section')

class SectionUpdateView(LoginRequiredMixin, UpdateView):
	model = Section
	fields =['sec_type']
	def get_context_data(self, **kwargs):
		context = super(SectionUpdateView, self).get_context_data(**kwargs)
		context["sec_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('section')

class CategoryCreateView(LoginRequiredMixin, CreateView):
	model = Category
	fields =['cat_type']
	def get_context_data(self, **kwargs):
		context = super(CategoryCreateView, self).get_context_data(**kwargs)
		context["cat_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('category')

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
	model = Category
	fields =['cat_type']
	def get_context_data(self, **kwargs):
		context = super(CategoryUpdateView, self).get_context_data(**kwargs)
		context["cat_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('category')

class LevelCreateView(LoginRequiredMixin, CreateView):
	model = Level
	fields =['lev_name']
	def get_context_data(self, **kwargs):
		context = super(LevelCreateView, self).get_context_data(**kwargs)
		context["levels"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('level')

class LevelUpdateView(LoginRequiredMixin, UpdateView):
	model = Level
	fields =['lev_name']
	def get_context_data(self, **kwargs):
		context = super(LevelUpdateView, self).get_context_data(**kwargs)
		context["levels"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('level')

class AccessCreateView(LoginRequiredMixin, CreateView):
	model = Access
	fields =['acc_type']
	def get_context_data(self, **kwargs):
		context = super(AccessCreateView, self).get_context_data(**kwargs)
		context["acc_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('access')

class AccessUpdateView(LoginRequiredMixin, UpdateView):
	model = Access
	fields =['acc_type']
	def get_context_data(self, **kwargs):
		context = super(AccessUpdateView, self).get_context_data(**kwargs)
		context["acc_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('access')

class RegstatusCreateView(LoginRequiredMixin, CreateView):
	model = Regstatus
	fields =['rs_type']
	def get_context_data(self, **kwargs):
		context = super(RegstatusCreateView, self).get_context_data(**kwargs)
		context["rs_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('regstatus')

class RegstatusUpdateView(LoginRequiredMixin, UpdateView):
	model = Regstatus
	fields =['rs_type']
	def get_context_data(self, **kwargs):
		context = super(RegstatusUpdateView, self).get_context_data(**kwargs)
		context["rs_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('regstatus')

class CennostatusCreateView(LoginRequiredMixin, CreateView):
	model = Cennostatus
	fields =['cns']
	def get_context_data(self, **kwargs):
		context = super(CennostatusCreateView, self).get_context_data(**kwargs)
		context["statuses"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('cennostatus')

class CennostatusUpdateView(LoginRequiredMixin, UpdateView):
	model = Cennostatus
	fields =['cns']
	def get_context_data(self, **kwargs):
		context = super(CennostatusUpdateView, self).get_context_data(**kwargs)
		context["statuses"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('cennostatus')

class SchtypeCreateView(LoginRequiredMixin, CreateView):
	model = Schtype
	fields =['sch_type']
	def get_context_data(self, **kwargs):
		context = super(SchtypeCreateView, self).get_context_data(**kwargs)
		context["types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('schtype')

class SchtypeUpdateView(LoginRequiredMixin, UpdateView):
	model = Schtype
	fields =['sch_type']
	def get_context_data(self, **kwargs):
		context = super(SchtypeUpdateView, self).get_context_data(**kwargs)
		context["types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('schtype')

class DistrictCreateView(LoginRequiredMixin, CreateView):
	model = District
	fields =['dis_name']
	def get_context_data(self, **kwargs):
		context = super(DistrictCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		districts = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["districts"] = districts.get_page(page)
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('district')

class DistrictUpdateView(LoginRequiredMixin, UpdateView):
	model = District
	fields =['dis_name']
	def get_context_data(self, **kwargs):
		context = super(DistrictUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		districts = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["districts"] = districts.get_page(page)
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('district')

class RegionCreateView(LoginRequiredMixin, CreateView):
	model = Region
	fields =['reg_name']
	def get_context_data(self, **kwargs):
		context = super(RegionCreateView, self).get_context_data(**kwargs)
		context["regions"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('region')

class RegionUpdateView(LoginRequiredMixin, UpdateView):
	model = Region
	fields =['reg_name']
	def get_context_data(self, **kwargs):
		context = super(RegionUpdateView, self).get_context_data(**kwargs)
		context["regions"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('region')

# Fac settings related views..................................................................................
# Fac settings related views..................................................................................

class FacilityTypeView(LoginRequiredMixin, CreateView):
	model = FacilityType
	fields =['facility_type']
	template_name = "ministry/facility_type_form.html"
	def get_context_data(self, **kwargs):
		context = super(FacilityTypeView, self).get_context_data(**kwargs)
		context["fac_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('factype')

class FacilityTypeUpdateView(LoginRequiredMixin, UpdateView):
	model = FacilityType
	fields =['facility_type']
	template_name = "ministry/facility_type_form.html"
	def get_context_data(self, **kwargs):
		context = super(FacilityTypeUpdateView, self).get_context_data(**kwargs)
		context["fac_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('factype')

class FacilityStatusView(LoginRequiredMixin, CreateView):
	model = FacilityStatus
	fields =['facility_status']
	template_name = "ministry/facility_status_form.html"
	def get_context_data(self, **kwargs):
		context = super(FacilityStatusView, self).get_context_data(**kwargs)
		context["statuses"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('facstatus')
		
class FacilityStatusUpdateView(LoginRequiredMixin, UpdateView):
	model = FacilityStatus
	fields =['facility_status']
	template_name = "ministry/facility_status_form.html"
	def get_context_data(self, **kwargs):
		context = super(FacilityStatusUpdateView, self).get_context_data(**kwargs)
		context["statuses"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('facstatus')

class TeacherStatusCreateView(LoginRequiredMixin, CreateView):
	model = TeacherStatus
	fields =['teacher_status']
	def get_context_data(self, **kwargs):
		context = super(TeacherStatusCreateView, self).get_context_data(**kwargs)
		context["statuses"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('teacher-status')


# Teacher settings related views..................................................................................
# Teacher settings views..................................................................................

class TeacherStatusUpdateView(LoginRequiredMixin, UpdateView):
	model = TeacherStatus
	fields =['teacher_status']
	def get_context_data(self, **kwargs):
		context = super(TeacherStatusUpdateView, self).get_context_data(**kwargs)
		context["statuses"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('teacher-status')

class GenderCreateView(LoginRequiredMixin, CreateView):
	model = Gender
	fields =['gender']
	def get_context_data(self, **kwargs):
		context = super(GenderCreateView, self).get_context_data(**kwargs)
		context["gender_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('gender')

class GenderUpdateView(LoginRequiredMixin, UpdateView):
	model = Gender
	fields =['gender']
	def get_context_data(self, **kwargs):
		context = super(GenderUpdateView, self).get_context_data(**kwargs)
		context["gender_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('gender')

# Resource related views..................................................................................
# Resource related views..................................................................................

class ResourceSourceCreateView(LoginRequiredMixin, CreateView):
	model = ResourceSource
	fields =['resource_source']
	def get_context_data(self, **kwargs):
		context = super(ResourceSourceCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		resource_sources = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["resource_sources"] = resource_sources.get_page(page)
		context["title"] = "Resources"
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('resource-source')

class ResourceSourceUpdateView(LoginRequiredMixin, UpdateView):
	model = ResourceSource
	fields =['resource_source']
	def get_context_data(self, **kwargs):
		context = super(ResourceSourceUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		resource_sources = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["resource_sources"] = resource_sources.get_page(page)
		context["title"] = "Resources"
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('resource-source')

class ResourceListView(ListView):
	model = Resource
	def get_context_data(self, **kwargs):
		context = super(ResourceListView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		resources = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["resources"] = resources.get_page(page)
		context["title"] = "Resources"
		return context

class ResourceTypeCreateView(LoginRequiredMixin, CreateView):
	model = ResourceType
	fields =['resource_type']
	def get_context_data(self, **kwargs):
		context = super(ResourceTypeCreateView, self).get_context_data(**kwargs)
		context["resource_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('resource-type')

class ResourceTypeUpdateView(LoginRequiredMixin, UpdateView):
	model = ResourceType
	fields =['resource_type']
	def get_context_data(self, **kwargs):
		context = super(ResourceTypeUpdateView, self).get_context_data(**kwargs)
		context["resource_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('resource-type')

class ResourceCreateView(LoginRequiredMixin, CreateView):
	model = Resource
	fields =['description','resource_type','source','quantity','amount','year','photo']
	def get_context_data(self, **kwargs):
		context = super(ResourceCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		resources = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["resources"] = resources.get_page(page)
		context["title"] = "Resources"
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.instance.user = self.request.user
			form.save()
			return redirect('resource')

class ResourceUpdateView(LoginRequiredMixin, UpdateView):
	model = Resource
	fields =['description','resource_type','source','quantity','amount','year','photo']
	def get_context_data(self, **kwargs):
		context = super(ResourceUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		resources = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["resources"] = resources.get_page(page)
		context["title"] = "Resources"
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.instance.user = self.request.user
			form.save()
			return redirect('resource')

class ResourceDetailView(DetailView):
	model = Resource
	def get_context_data(self, **kwargs):
		context = super(ResourceDetailView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		allocated = Paginator(AllocateResource.objects.filter(resource=self.object).order_by('-id'), 10)
		context["allocated"] = allocated.get_page(page)
		return context

class AllocateResourceCreateView(LoginRequiredMixin, CreateView):
	model = AllocateResource
	fields =['resource','school','quantity','amount','date_allocated','date_valid','year']
	def get_context_data(self, **kwargs):
		context = super(AllocateResourceCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		allocate_resources = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["allocate_resources"] = allocate_resources.get_page(page)
		context["title"] = "Resources"
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.instance.user = self.request.user
			form.save(commit=False)
			resource = form.cleaned_data.get('resource')
			amount = form.cleaned_data.get('amount')
			qty = form.cleaned_data.get('quantity')
			amount_all = AllocateResource.objects.filter()
			return redirect('allocate-resource')

class AllocateResourceUpdateView(LoginRequiredMixin, UpdateView):
	model = AllocateResource
	fields =['resource','school','quantity','amount','date_allocated','date_valid','year']
	def get_context_data(self, **kwargs):
		context = super(AllocateResourceUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		allocate_resources = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["allocate_resources"] = allocate_resources.get_page(page)
		context["title"] = "Resources"
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.instance.user = self.request.user
			form.save()
			return redirect('allocate-resource')

class ResourceListView(ListView):
	model = Resource
	context_object_name = 'resources'
	ordering = ['-id']

class AllocateResourceListView(ListView):
	model = AllocateResource
	def get_context_data(self, **kwargs):
		context = super(AllocateResourceListView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		allocate_resources = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["allocate_resources"] = allocate_resources.get_page(page)
		context["title"] = "Resources"
		return context

class ProductCreateView(LoginRequiredMixin, CreateView):
	model = Product
	fields =['title','description','price','phone_contact','photo']
	def get_context_data(self, **kwargs):
		context = super(ProductCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		products = Paginator(self.model.objects.filter(user=self.request.user).order_by('-id'), 10)
		context["products"] = products.get_page(page)
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.instance.user = self.request.user
			form.save()
			return redirect('product')

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Product
	fields =['title','description','price','phone_contact','status','photo']
	def get_context_data(self, **kwargs):
		context = super(ProductUpdateView, self).get_context_data(**kwargs)
		context["products"] = self.model.objects.filter(user=self.request.user).order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.instance.user = self.request.user
			form.save()
			return redirect('product')
	def test_func(self):
		product = self.get_object()
		if self.request.user == product.user:
			return True
		return False

class ProductListView(ListView):
	model = Product
	context_object_name = 'products'
	ordering = ['-id']

class UserProducts(ListView):
	model = Product
	def get_context_data(self, **kwargs):
		context = super(UserProducts, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		products = pagenator = Paginator(self.model.objects.filter(user=self.request.user).order_by('-id'), 2)
		context["products"] = products.get_page(page)
		return context

class ProductDetailView(DetailView):
	model = Product

class ProductStatusCreateView(LoginRequiredMixin, CreateView):
	model = ProductStatus
	fields =['status']
	def get_context_data(self, **kwargs):
		context = super(ProductStatusCreateView, self).get_context_data(**kwargs)
		context["statuses"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('product-status')

class ProductStatusUpdateView(LoginRequiredMixin, UpdateView):
	model = ProductStatus
	fields =['status']
	def get_context_data(self, **kwargs):
		context = super(ProductStatusUpdateView, self).get_context_data(**kwargs)
		context["statuses"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('product-status')

class SubjectCreateView(LoginRequiredMixin, CreateView):
	model = Subject
	template_name = "ministry/subject_form.html"
	fields =['subject_code','subject_name']
	def get_context_data(self, **kwargs):
		context = super(SubjectCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		subjects = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["subjects"] = subjects.get_page(page)
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.instance.user = self.request.user
			form.save()
			return redirect('subject')

class SubjectUpdateView(LoginRequiredMixin, UpdateView):
	model = Subject
	template_name = "ministry/subject_form.html"
	fields =['subject_code','subject_name']
	def get_context_data(self, **kwargs):
		context = super(SubjectUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		subjects = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["subjects"] = subjects.get_page(page)
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.instance.user = self.request.user
			form.save()
			return redirect('subject')

@login_required
def ministry_add_students(request, pk):
	school = School.objects.get(pk=pk)
	classes = None
	ages = None
	if(school.level_id==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(school.level_id==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(school.level_id==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	if(school.level_id==1):
		ages = AgeGroup.objects.filter(pk__lte=4)
	elif(school.level_id==2):
		ages = AgeGroup.objects.filter(pk__gte=5, pk__lte=12,)
	elif(school.level_id==3):
		ages = AgeGroup.objects.filter(pk__gte=13, pk__lte=22,)
	else:
		ages = AgeGroup.objects.filter(pk__gt=22,)
	enrolment_list = []
	total_rows = len(classes)*len(ages)
	if request.method == 'POST':
		student_form = StudentCreateForm(request.POST, )
		if student_form.is_valid():
			year = student_form.cleaned_data.get('year')
			class_name = request.POST.getlist('class_name')
			age = request.POST.getlist('age')
			girls = request.POST.getlist('girls')
			boys = request.POST.getlist('boys')
			std_records = [class_name, age, boys, girls]
			enrolment_list.append(std_records)
			for c, a, g, b in enrolment_list:
				some_data = []
				for i in range(0, total_rows):
					if g[i]=='':
						g[i]=0
					if b[i]=='':
						b[i]=0
					if int(g[i])>0 or int(b[i])>0:
						some_data.append(Student(**{
											'year' : year,
											'user' : request.user,
											'school' : school,
											'class_name' : Class.objects.get(pk=c[i]),
											'age' : AgeGroup.objects.get(pk=a[i]),
											'girls' : g[i],
											'boys' : b[i],
											}))
			# Student.objects.bulk_create(some_data)
			try:
				Student.objects.bulk_create(some_data)
				messages.success(request, f'Enrolments for {year} have been recorded. Proceed to record Repeaters')
				
			except Exception:
				messages.warning(request, f'ERROR! May be some enrolments of {year} are already recorded. Only Fill the ones that are not yet entered.')				
	else:
		student_form = StudentCreateForm()
	context = {
	'title': 'Students',
	'sub_title': 'Enrolment',
	'student_form': student_form,
	'classes': classes,
	'ages': ages,
	'school': school,
	}
	return render(request, 'ministry/ministry_add_students.html', context)

@login_required
def enrolments(request, pk):
	level = Level.objects.get(pk=pk)
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = Student.objects.values('school__level','year','class_name','age').filter(school__level=level, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys')).order_by('age')
	students_by_class = Student.objects.values('class_name').filter(school__level=level, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	students_by_age = Student.objects.values('age').filter(school__level=level, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	total_students = Student.objects.filter(school__level=level, 
		year=year).aggregate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	classes = None
	ages = None
	if(pk==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(pk==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(pk==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	if(pk==1):
		ages = AgeGroup.objects.filter(pk__lte=4)
	elif(pk==2):
		ages = AgeGroup.objects.filter(pk__gte=5, pk__lte=12,)
	elif(pk==3):
		ages = AgeGroup.objects.filter(pk__gte=13, pk__lte=22,)
	else:
		ages = AgeGroup.objects.filter(pk__gt=22,)

	context = {
	'title': 'Students',
	'sub_title': 'Enrolment',
	'students': students,
	'classes': classes,
	'ages': ages,
	'students_by_class': students_by_class,
	'students_by_age': students_by_age,
	'total_students': total_students,
	'year':year,
	'level':level,
	}
	return render(request, 'ministry/students.html', context)

@login_required
def repeaters(request, pk):
	level = Level.objects.get(pk=pk)
	classes = None
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = Repeater.objects.values('school__level','year','class_name').filter(school__level=level, year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	students_by_class = Repeater.objects.filter(school__level=level, 
		year=year).aggregate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	if(pk==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(pk==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(pk==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	context = {
	'title': 'Students',
	'sub_title': 'Repeaters',
	'classes': classes,
	'students': students,
	'students_by_class': students_by_class,
	'year': year,
	'level':level,
	}
	return render(request, 'ministry/students.html', context)

@login_required
def nationality(request, pk):
	level = Level.objects.get(pk=pk)
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = Nationality.objects.values('school__level','year','class_name','country').filter(school__level=level, year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys')).order_by('country_id',)
	students_by_class = Nationality.objects.values('class_name').filter(school__level=level, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	students_by_country = Nationality.objects.values('country').filter(school__level=level, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	total_students = Nationality.objects.filter(school__level=level, 
		year=year).aggregate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	classes = None
	countries = Country.objects.all()
	if(pk==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(pk==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(pk==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	context = {
	'title': 'Students',
	'sub_title': 'Nationality',
	'students': students,
	'classes': classes,
	'countries': countries,
	'students_by_class': students_by_class,
	'students_by_country': students_by_country,
	'total_students': total_students,
	'year':year,
	'level':level,
	}
	return render(request, 'ministry/students.html', context)

@login_required
def proposed_intake(request, pk):
	level = Level.objects.get(pk=pk)
	classes = None
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = ProposedIntake.objects.values('school__level','year','class_name').filter(school__level=level, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	students_by_class = ProposedIntake.objects.filter(school__level=level, 
		year=year).aggregate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	if(pk==1):
		classes = IntakeClass.objects.filter(pk__lte=1)
	elif(pk==2):
		classes = IntakeClass.objects.filter(pk__gte=2, pk__lte=2,)
	elif(pk==3):
		classes = IntakeClass.objects.filter(pk__gte=3, pk__lte=5,)
	else:
		classes = IntakeClass.objects.filter(pk__gt=5,)

	context = {
	'title': 'Students',
	'sub_title': 'Proposed Intake',
	'classes': classes,
	'students': students,
	'students_by_class': students_by_class,
	'year': year,
	'level':level,
	}
	return render(request, 'ministry/students.html', context)

@login_required
def physical_streams(request, pk):
	level = Level.objects.get(pk=pk)
	classes = None
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = PhysicalStream.objects.values('school__level','year','class_name').filter(school__level=level, year=year).annotate(total_streams=Sum('streams'))
	students_by_stream = PhysicalStream.objects.filter(school__level=level, 
		year=year).aggregate(total_streams=Sum('streams'))
	if(pk==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(pk==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(pk==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	context = {
	'title': 'Students',
	'sub_title': 'Physical Streams',
	'classes': classes,
	'students': students,
	'students_by_stream': students_by_stream,
	'year': year,
	'level':level,
	}
	return render(request, 'ministry/students.html', context)

@login_required
def orphans(request, pk):
	level = Level.objects.get(pk=pk)
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = Orphan.objects.values('school__level','year','class_name','status').filter(school__level=level, year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	students_by_class = Orphan.objects.values('class_name').filter(school__level=level, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	students_by_status = Orphan.objects.values('status').filter(school__level=level, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	total_students = Orphan.objects.filter(school__level=level, 
		year=year).aggregate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	classes = None
	statuses = OrphanStatus.objects.all()
	if(pk==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(pk==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(pk==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	context = {
	'title': 'Students',
	'sub_title': 'Orphans',
	'students': students,
	'classes': classes,
	'statuses': statuses,
	'students_by_class': students_by_class,
	'students_by_status': students_by_status,
	'total_students': total_students,
	'year':year,
	'level':level,
	}
	return render(request, 'ministry/students.html', context)

@login_required
def special_needs(request, pk):
	level = Level.objects.get(pk=pk)
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = SpecialNeed.objects.values('school__level','year','class_name','status').filter(school__level=level, year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	students_by_class = SpecialNeed.objects.values('class_name').filter(school__level=level, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	students_by_status = SpecialNeed.objects.values('status').filter(school__level=level, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	total_students = SpecialNeed.objects.filter(school__level=level, 
		year=year).aggregate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	classes = None
	statuses = SpecialNeedStatus.objects.all()
	if(pk==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(pk==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(pk==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	context = {
	'title': 'Students',
	'sub_title': 'Special Needs',
	'students': students,
	'classes': classes,
	'statuses': statuses,
	'students_by_class': students_by_class,
	'students_by_status': students_by_status,
	'total_students': total_students,
	'year':year,
	'level':level,
	}
	return render(request, 'ministry/students.html', context)

@login_required
def new_entrants(request, pk):
	level = Level.objects.get(pk=pk)
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = NewEntrant.objects.values('school__level','year','age').filter(school__level=level, year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	students_by_age = NewEntrant.objects.filter(school__level=level, 
		year=year).aggregate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	ages = None
	if(pk==1):
		ages = AgeGroup.objects.filter(pk__lte=4)
	elif(pk==2):
		ages = AgeGroup.objects.filter(pk__gte=5, pk__lte=10,)
	elif(pk==3):
		ages = AgeGroup.objects.filter(pk__gte=13, pk__lte=20,)
	else:
		ages = AgeGroup.objects.filter(pk__gt=22,)

	classes = None
	if(pk==1):
		classes = Class.objects.get(pk=1)
	elif(pk==2):
		classes = Class.objects.get(pk=4)
	elif(pk==3):
		classes = Class.objects.get(pk=11)
	else:
		classes = Class.objects.get(pk=17)

	context = {
	'title': 'Students',
	'sub_title': 'New Entrants',
	'classes': classes,
	'ages': ages,
	'students': students,
	'students_by_age': students_by_age,
	'year': year,
	'level':level,
	}
	return render(request, 'ministry/students.html', context)

@login_required
def seating_and_writing_space(request, pk):
	level = Level.objects.get(pk=pk)
	classes = None
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = SeatingAndWritingSpace.objects.values('school__level','year','class_name').filter(school__level=level, year=year).annotate(total_pupils=Sum('pupils'))
	students_by_class = SeatingAndWritingSpace.objects.filter(school__level=level, 
		year=year).aggregate(total_pupils=Sum('pupils'))
	if(pk==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(pk==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(pk==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	context = {
	'title': 'Students',
	'sub_title': 'Seating and Writing Space',
	'classes': classes,
	'students': students,
	'students_by_class': students_by_class,
	'year': year,
	'level':level,
	}
	return render(request, 'ministry/students.html', context)

@login_required
def transfered_students(request, pk):
	level = Level.objects.get(pk=pk)
	classes = None
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = TransferedStudent.objects.values('school__level','year','class_name').filter(school__level=level, year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	students_by_class = TransferedStudent.objects.filter(school__level=level, 
		year=year).aggregate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	if(pk==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(pk==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(pk==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	context = {
	'title': 'Students',
	'sub_title': 'Transfered Students',
	'classes': classes,
	'students': students,
	'students_by_class': students_by_class,
	'year': year,
	'level':level,
	}
	return render(request, 'ministry/students.html', context)

@login_required
def examinations(request, pk):
	level = Level.objects.get(pk=pk)
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = Examination.objects.values('school__level','year','class_name','term').filter(school__level=level, year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	students_by_term = Examination.objects.values('term').filter(school__level=level, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	classes = None
	terms = Term.objects.all()
	if(pk==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(pk==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(pk==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	context = {
	'title': 'Students',
	'sub_title': 'Examinations',
	'students': students,
	'classes': classes,
	'terms': terms,
	'students_by_term': students_by_term,
	'year':year,
	'level':level,
	}
	return render(request, 'ministry/students.html', context)

@login_required
def view_schools(request, pk):
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
	return render(request, 'ministry/school_list.html', context)

def schools_region_chart(request, pk):
	level = Level.objects.get(pk=pk)
	labels = []
	data = []
	schools_in_region = School.objects.values('parish__district__region__reg_name').annotate(total_schools=Count('parish__district__region')).filter(level=level).order_by('-total_schools')
	for school in schools_in_region:
		labels.append(school['parish__district__region__reg_name'])
		data.append(school['total_schools'])

	return JsonResponse(data={'labels': labels, 'data': data, })

def schools_year_chart(request, pk):
	level = Level.objects.get(pk=pk)
	labels = []
	data = []
	year1 = School.objects.filter(level=level, yr_est__lte=datetime.datetime.now().year-4).count()
	year2 = School.objects.filter(level=level, yr_est__lte=datetime.datetime.now().year-3).count()
	year3 = School.objects.filter(level=level, yr_est__lte=datetime.datetime.now().year-2).count()
	year4 = School.objects.filter(level=level, yr_est__lte=datetime.datetime.now().year-1).count()
	year5 = School.objects.filter(level=level, yr_est__lte=datetime.datetime.now().year).count()
	labels.append(datetime.datetime.now().year-4)
	labels.append(datetime.datetime.now().year-3)
	labels.append(datetime.datetime.now().year-2)
	labels.append(datetime.datetime.now().year-1)
	labels.append(datetime.datetime.now().year)
	data.append(year1)
	data.append(year2)
	data.append(year3)
	data.append(year4)
	data.append(year5)

	return JsonResponse(data={'labels': labels, 'data': data, })

def operation_status_chart(request, pk):
	level = Level.objects.get(pk=pk)
	labels = []
	data = []
	schools = School.objects.values('operation_status__sch_type').annotate(total_schools=Count('operation_status')).filter(level=level).order_by('-total_schools')
	for school in schools:
		labels.append(school['operation_status__sch_type'])
		data.append(school['total_schools'])

	return JsonResponse(data={'labels': labels, 'data': data, })

def founder_chart(request, pk):
	level = Level.objects.get(pk=pk)
	labels = []
	data = []
	schools = School.objects.values('founder__own_type').annotate(total_schools=Count('founder')).filter(level=level).order_by('-total_schools')
	for school in schools:
		labels.append(school['founder__own_type'])
		data.append(school['total_schools'])
	return JsonResponse(data={'labels': labels, 'data': data, })

def funder_chart(request, pk):
	level = Level.objects.get(pk=pk)
	labels = []
	data = []
	schools = School.objects.values('funder__funder_name').annotate(total_schools=Count('funder')).filter(level=level).order_by('-total_schools')
	for school in schools:
		labels.append(school['funder__funder_name'])
		data.append(school['total_schools'])
	return JsonResponse(data={'labels': labels, 'data': data, })

def category_chart(request, pk):
	level = Level.objects.get(pk=pk)
	labels = []
	data = []
	schools = School.objects.values('category__cat_type').annotate(total_schools=Count('category')).filter(level=level).order_by('-total_schools')
	for school in schools:
		labels.append(school['category__cat_type'])
		data.append(school['total_schools'])
	return JsonResponse(data={'labels': labels, 'data': data, })

def section_chart(request, pk):
	level = Level.objects.get(pk=pk)
	labels = []
	data = []
	schools = School.objects.values('section__sec_type').annotate(total_schools=Count('section')).filter(level=level).order_by('-total_schools')
	for school in schools:
		labels.append(school['section__sec_type'])
		data.append(school['total_schools'])
	return JsonResponse(data={'labels': labels, 'data': data, })

def registry_status_chart(request, pk):
	level = Level.objects.get(pk=pk)
	labels = []
	data = []
	schools = School.objects.values('regstatus__reg_status').annotate(total_schools=Count('regstatus')).filter(level=level).order_by('-total_schools')
	for school in schools:
		labels.append(school['regstatus__reg_status'])
		data.append(school['total_schools'])
	return JsonResponse(data={'labels': labels, 'data': data, })

def rural_urban_chart(request, pk):
	level = Level.objects.get(pk=pk)
	labels = []
	data = []
	schools = School.objects.values('rural_urban__rural_urban').annotate(total_schools=Count('rural_urban')).filter(level=level).order_by('-total_schools')
	for school in schools:
		labels.append(school['rural_urban__rural_urban'])
		data.append(school['total_schools'])
	return JsonResponse(data={'labels': labels, 'data': data, })

def access_chart(request, pk):
	level = Level.objects.get(pk=pk)
	labels = []
	data = []
	schools = School.objects.values('access__acc_type').annotate(total_schools=Count('access')).filter(level=level).order_by('-total_schools')
	for school in schools:
		labels.append(school['access__acc_type'])
		data.append(school['total_schools'])
	return JsonResponse(data={'labels': labels, 'data': data, })

def registry_status_chart(request, pk):
	level = Level.objects.get(pk=pk)
	labels = []
	data = []
	schools = School.objects.values('regstatus__rs_type').annotate(total_schools=Count('regstatus')).filter(level=level).order_by('-total_schools')
	for school in schools:
		labels.append(school['regstatus__rs_type'])
		data.append(school['total_schools'])
	return JsonResponse(data={'labels': labels, 'data': data, })

def nearest_school_chart(request, pk):
	level = Level.objects.get(pk=pk)
	labels = []
	data = []
	schools = School.objects.values('distance_to_nearest_school__distance').annotate(total_schools=Count('distance_to_nearest_school')).filter(level=level).order_by('-total_schools')
	for school in schools:
		labels.append(school['distance_to_nearest_school__distance'])
		data.append(school['total_schools'])
	return JsonResponse(data={'labels': labels, 'data': data, })

def deo_office_chart(request, pk):
	level = Level.objects.get(pk=pk)
	labels = []
	data = []
	schools = School.objects.values('distance_to_deo_office__distance').annotate(total_schools=Count('distance_to_deo_office')).filter(level=level).order_by('-total_schools')
	for school in schools:
		labels.append(school['distance_to_deo_office__distance'])
		data.append(school['total_schools'])
	return JsonResponse(data={'labels': labels, 'data': data, })


@login_required
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
	return render(request, 'ministry/school_list.html', context)

@login_required
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
	return render(request, 'ministry/school_list.html', context)

@login_required
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
	return render(request, 'ministry/school_list.html', context)

@login_required
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
	return render(request, 'ministry/school_list.html', context)

@login_required
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
	return render(request, 'ministry/school_list.html', context)

@login_required
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
	return render(request, 'ministry/school_list.html', context)

@login_required
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
	return render(request, 'ministry/school_list.html', context)

@login_required
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
	return render(request, 'ministry/school_list.html', context)

@login_required
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
	return render(request, 'ministry/school_list.html', context)

@login_required
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
	return render(request, 'ministry/school_list.html', context)

@login_required
def teachers(request):
	return render(request, 'ministry/teachers.html', {'title': 'Teachers'})

@login_required
def region_teachers(request, pk):
	level = Level.objects.get(pk=pk)
	schtypes = Schtype.objects.all()
	regions = Region.objects.all()
	f_teachers = Teacher.objects.values('school__parish__district__region',
		'school__operation_status').filter(school__level=level, gender=2).annotate(total_girls=Count('school__parish__district__region'))
	m_teachers = Teacher.objects.values('school__parish__district__region',
		'school__operation_status').filter(school__level=level, gender=1).annotate(total_boys=Count('school__parish__district__region'))
	f_teachers_region = Teacher.objects.values('school__parish__district__region',
		).filter(school__level=level, gender=2).annotate(total_girls=Count('school__parish__district__region'))
	m_teachers_region = Teacher.objects.values('school__parish__district__region',
		).filter(school__level=level, gender=1).annotate(total_boys=Count('school__parish__district__region'))
	f_teachers_status = Teacher.objects.values('school__operation_status').filter(school__level=level, 
		gender=2).annotate(total_girls=Count('school__operation_status'))
	m_teachers_status = Teacher.objects.values('school__operation_status').filter(school__level=level, 
		gender=1).annotate(total_boys=Count('school__operation_status'))
	teachers_total = Teacher.objects.values('gender').filter(school__level=level).annotate(total_teachers=Count('gender'))

	context = {
	'title': 'Teachers',
	'sub_title': 'Region',
	'schtypes': schtypes,
	'regions': regions,
	'f_teachers': f_teachers,
	'm_teachers': m_teachers,
	'f_teachers_region': f_teachers_region,
	'm_teachers_region': m_teachers_region,
	'f_teachers_status': f_teachers_status,
	'm_teachers_status': m_teachers_status,
	'teachers_total': teachers_total,
	'level':level,
	}
	return render(request, 'ministry/teachers.html', context)

@login_required
def qualification_teachers(request, pk):
	level = Level.objects.get(pk=pk)
	schtypes = Schtype.objects.all()
	professions = TeacherProfession.objects.all()
	f_teachers = Teacher.objects.values('profession',
		'school__operation_status').filter(school__level=level, gender=2).annotate(total_girls=Count('profession'))
	m_teachers = Teacher.objects.values('profession',
		'school__operation_status').filter(school__level=level, gender=1).annotate(total_boys=Count('profession'))
	f_teachers_professions = Teacher.objects.values('profession',
		).filter(school__level=level, gender=2).annotate(total_girls=Count('profession'))
	m_teachers_professions = Teacher.objects.values('profession',
		).filter(school__level=level, gender=1).annotate(total_boys=Count('profession'))
	f_teachers_status = Teacher.objects.values('school__operation_status').filter(school__level=level, 
		gender=2).annotate(total_girls=Count('school__operation_status'))
	m_teachers_status = Teacher.objects.values('school__operation_status').filter(school__level=level, 
		gender=1).annotate(total_boys=Count('school__operation_status'))
	teachers_total = Teacher.objects.values('gender').filter(school__level=level).annotate(total_teachers=Count('gender'))

	context = {
	'title': 'Teachers',
	'sub_title': 'Qualification',
	'schtypes': schtypes,
	'regions': professions,
	'f_teachers': f_teachers,
	'm_teachers': m_teachers,
	'f_teachers_region': f_teachers_professions,
	'm_teachers_region': m_teachers_professions,
	'f_teachers_status': f_teachers_status,
	'm_teachers_status': m_teachers_status,
	'teachers_total': teachers_total,
	'level':level,
	}
	return render(request, 'ministry/teachers.html', context)

@login_required
def education_teachers(request, pk):
	level = Level.objects.get(pk=pk)
	schtypes = Schtype.objects.all()
	educations = TeacherEducation.objects.all()
	f_teachers = Teacher.objects.values('education',
		'school__operation_status').filter(school__level=level, gender=2).annotate(total_girls=Count('profession'))
	m_teachers = Teacher.objects.values('education',
		'school__operation_status').filter(school__level=level, gender=1).annotate(total_boys=Count('profession'))
	f_teachers_professions = Teacher.objects.values('education',
		).filter(school__level=level, gender=2).annotate(total_girls=Count('education'))
	m_teachers_professions = Teacher.objects.values('education',
		).filter(school__level=level, gender=1).annotate(total_boys=Count('education'))
	f_teachers_status = Teacher.objects.values('school__operation_status').filter(school__level=level, 
		gender=2).annotate(total_girls=Count('school__operation_status'))
	m_teachers_status = Teacher.objects.values('school__operation_status').filter(school__level=level, 
		gender=1).annotate(total_boys=Count('school__operation_status'))
	teachers_total = Teacher.objects.values('gender').filter(school__level=level).annotate(total_teachers=Count('gender'))

	context = {
	'title': 'Teachers',
	'sub_title': 'Education',
	'schtypes': schtypes,
	'regions': educations,
	'f_teachers': f_teachers,
	'm_teachers': m_teachers,
	'f_teachers_region': f_teachers_professions,
	'm_teachers_region': m_teachers_professions,
	'f_teachers_status': f_teachers_status,
	'm_teachers_status': m_teachers_status,
	'teachers_total': teachers_total,
	'level':level,
	}
	return render(request, 'ministry/teachers.html', context)

@login_required
def left_teachers(request, pk):
	level = Level.objects.get(pk=pk)
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	teachers = LeftTeacher.objects.values('school__level','year','school__operation_status','reason').filter(school__level=level, year=year).annotate(total_girls=Sum('female'), total_boys=Sum('male'))
	teachers_by_reason = LeftTeacher.objects.values('reason').filter(school__level=level, 
		year=year).annotate(total_girls=Sum('female'), total_boys=Sum('male'))
	teachers_by_status = LeftTeacher.objects.values('school__operation_status').filter(school__level=level, 
		year=year).annotate(total_girls=Sum('female'), total_boys=Sum('male'))
	total_teachers = LeftTeacher.objects.filter(school__level=level, 
		year=year).aggregate(total_girls=Sum('female'), total_boys=Sum('male'))
	statuses = Schtype.objects.all()
	reasons = Reason.objects.all()

	context = {
	'title': 'Teachers',
	'sub_title': 'Teachers Leaving',
	'teachers': teachers,
	'statuses': statuses,
	'reasons': reasons,
	'teachers_by_reason': teachers_by_reason,
	'teachers_by_status': teachers_by_status,
	'total_teachers':total_teachers,
	'year':year,
	'level':level,
	}
	return render(request, 'ministry/teachers.html', context)

@login_required
def non_teaching_staff(request, pk):
	level = Level.objects.get(pk=pk)
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	teachers = NonTeachingStaff.objects.values('school__level','year','school__operation_status','staff_type').filter(school__level=level, year=year).annotate(total_girls=Sum('female'), total_boys=Sum('male'))
	teachers_by_type = NonTeachingStaff.objects.values('staff_type').filter(school__level=level, 
		year=year).annotate(total_girls=Sum('female'), total_boys=Sum('male'))
	teachers_by_status = NonTeachingStaff.objects.values('school__operation_status').filter(school__level=level, 
		year=year).annotate(total_girls=Sum('female'), total_boys=Sum('male'))
	total_teachers = NonTeachingStaff.objects.filter(school__level=level, 
		year=year).aggregate(total_girls=Sum('female'), total_boys=Sum('male'))
	statuses = Schtype.objects.all()
	types = StaffType.objects.all()

	context = {
	'title': 'Teachers',
	'sub_title': 'Non-Teaching Staff',
	'teachers': teachers,
	'statuses': statuses,
	'types': types,
	'teachers_by_type': teachers_by_type,
	'teachers_by_status': teachers_by_status,
	'total_teachers':total_teachers,
	'year':year,
	'level':level,
	}
	return render(request, 'ministry/teachers.html', context)

@login_required
def non_teaching_staff(request, pk):
	level = Level.objects.get(pk=pk)
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	teachers = NonTeachingStaff.objects.values('school__level','year','school__operation_status','staff_type').filter(school__level=level, year=year).annotate(total_girls=Sum('female'), total_boys=Sum('male'))
	teachers_by_type = NonTeachingStaff.objects.values('staff_type').filter(school__level=level, 
		year=year).annotate(total_girls=Sum('female'), total_boys=Sum('male'))
	teachers_by_status = NonTeachingStaff.objects.values('school__operation_status').filter(school__level=level, 
		year=year).annotate(total_girls=Sum('female'), total_boys=Sum('male'))
	total_teachers = NonTeachingStaff.objects.filter(school__level=level, 
		year=year).aggregate(total_girls=Sum('female'), total_boys=Sum('male'))
	statuses = Schtype.objects.all()
	types = StaffType.objects.all()

	context = {
	'title': 'Teachers',
	'sub_title': 'Non-Teaching Staff',
	'teachers': teachers,
	'statuses': statuses,
	'types': types,
	'teachers_by_type': teachers_by_type,
	'teachers_by_status': teachers_by_status,
	'total_teachers':total_teachers,
	'year':year,
	'level':level,
	}
	return render(request, 'ministry/teachers.html', context)

@login_required
def building_rooms(request, pk):
	level = Level.objects.get(pk=pk)
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	rooms = Building.objects.values('school__level','year','school__operation_status','room_state',
		'room_state','room_type','room_status').filter(school__level=level, 
		year=year).annotate(total_permanent=Sum('permanent'), total_temporary=Sum('temporary'))
	rooms_by_type = Building.objects.values('school__level','year','room_type',).filter(school__level=level, 
		year=year).annotate(total_permanent=Sum('permanent'), total_temporary=Sum('temporary'))
	rooms_by_status = Building.objects.values('school__level','year','school__operation_status','room_state',
		'room_state','room_status').filter(school__level=level, 
		year=year).annotate(total_permanent=Sum('permanent'), total_temporary=Sum('temporary'))
	rooms_total = Building.objects.filter(school__level=level,year=year).aggregate(total_permanent=Sum('permanent'), 
		total_temporary=Sum('temporary'))
	operation_statuses = Schtype.objects.all()
	types = RoomType.objects.all()
	states = RoomState.objects.all()
	statuses = RoomStatus.objects.all()
	context = {
	'title': 'Infrastructure',
	'sub_title': 'Rooms',
	'types': types,
	'states': states,
	'statuses': statuses,
	'level': level,
	'rooms': rooms,
	'rooms_by_type': rooms_by_type,
	'rooms_by_status': rooms_by_status,
	'rooms_total': rooms_total,
	'year': year,
	'operation_statuses': operation_statuses,
	}
	return render(request, 'ministry/infrastructure.html', context)

@login_required
def rooms_under_construction(request, pk):
	level = Level.objects.get(pk=pk)
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	rooms = UnderConstructionBuilding.objects.values('school__level','year','school__operation_status',
		'room_completion','room_type').filter(school__level=level, year=year).annotate(total_rooms=Sum('rooms'))
	rooms_by_type = UnderConstructionBuilding.objects.values('school__level','year','room_type',).filter(school__level=level, 
		year=year).annotate(total_rooms=Sum('rooms'))
	rooms_by_completion = UnderConstructionBuilding.objects.values('school__level','year','school__operation_status',
		'room_completion').filter(school__level=level, year=year).annotate(total_rooms=Sum('rooms'))
	rooms_total = UnderConstructionBuilding.objects.filter(school__level=level,year=year).aggregate(total_rooms=Sum('rooms'))
	operation_statuses = Schtype.objects.all()
	types = RoomType.objects.all()
	states = RoomCompletion.objects.all()
	context = {
	'title': 'Infrastructure',
	'sub_title': 'Rooms Under Construction',
	'types': types,
	'states': states,
	'level': level,
	'rooms': rooms,
	'rooms_by_type': rooms_by_type,
	'rooms_by_completion': rooms_by_completion,
	'rooms_total': rooms_total,
	'year': year,
	'operation_statuses': operation_statuses,
	}
	return render(request, 'ministry/infrastructure.html', context)

@login_required
def rooms_needed(request, pk):
	level = Level.objects.get(pk=pk)
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	rooms = NeededBuilding.objects.values('school__level','year','school__operation_status',
		'room_type').filter(school__level=level, year=year).annotate(total_rooms=Sum('rooms'))
	rooms_by_type = NeededBuilding.objects.values('school__level','year','room_type',).filter(school__level=level, 
		year=year).annotate(total_rooms=Sum('rooms'))
	rooms_by_status = NeededBuilding.objects.values('school__level','year','school__operation_status',
		).filter(school__level=level, year=year).annotate(total_rooms=Sum('rooms'))
	rooms_total = NeededBuilding.objects.filter(school__level=level,year=year).aggregate(total_rooms=Sum('rooms'))
	operation_statuses = Schtype.objects.all()
	types = RoomType.objects.all()
	context = {
	'title': 'Infrastructure',
	'sub_title': 'Rooms Needed',
	'types': types,
	'level': level,
	'rooms': rooms,
	'rooms_by_type': rooms_by_type,
	'rooms_by_status': rooms_by_status,
	'rooms_total': rooms_total,
	'year': year,
	'operation_statuses': operation_statuses,
	}
	return render(request, 'ministry/infrastructure.html', context)

@login_required
def deos(request):
	return render(request, 'ministry/deos.html', {'title': 'DEOs'})

def resources(request):
	return render(request, 'ministry/resources.html', {'title': 'Resources'})

def marketing(request):
	product_list = Product.objects.filter(status=1).order_by('-id')
	products_sold = Product.objects.filter(user=request.user, status=2).order_by('-id')
	paginator = Paginator(product_list, 5)
	page = request.GET.get('page')
	products = paginator.get_page(page)
	return render(request, 'ministry/marketing.html', {'title': 'Marketing', 'products':products, 'products_sold':products_sold})

def communication(request):
	return render(request, 'ministry/communication.html', {'title': 'Communication'})

def settings(request):
	return render(request, 'ministry/settings.html', {'title': 'Settings'})

@login_required
def home(request):
	primary_schools = School.objects.filter(level=2).count()
	secondary_schools = School.objects.filter(level=3).count()
	tertiary_schools = School.objects.filter(level=4).count()
	universities = School.objects.filter(level=5).count()
	all_deos = Deo.objects.count()
	all_teachers = Teacher.objects.count()
	all_resources = Resource.objects.count()
	all_trtransfer = TransferTeacher.objects.count()
	all_deotransfer = TransferDeo.objects.count()
	primary_labels = []
	primary_data = []
	primary_queryset = School.objects.values('founder__own_type').annotate(total_schools=Count('founder')).filter(level=2).order_by('-total_schools')
	for school in primary_queryset:
		primary_labels.append(school['founder__own_type'])
		primary_data.append(school['total_schools'])

	secondary_labels = []
	secondary_data = []
	secondary_queryset = School.objects.values('founder__own_type').annotate(total_schools=Count('founder')).filter(level=3).order_by('-total_schools')
	for school in secondary_queryset:
		secondary_labels.append(school['founder__own_type'])
		secondary_data.append(school['total_schools'])

	tertiary_labels = []
	tertiary_data = []
	tertiary_queryset = School.objects.values('founder__own_type').annotate(total_schools=Count('founder')).filter(level=4).order_by('-total_schools')
	for school in tertiary_queryset:
		tertiary_labels.append(school['founder__own_type'])
		tertiary_data.append(school['total_schools'])

	university_labels = []
	university_data = []
	university_queryset = School.objects.values('founder__own_type').annotate(total_schools=Count('founder')).filter(level=5).order_by('-total_schools')
	for school in university_queryset:
		university_labels.append(school['founder__own_type'])
		university_data.append(school['total_schools'])

	context = {'title': 'Home', 
		'primary_schools':primary_schools, 
		'secondary_schools':secondary_schools, 
		'tertiary_schools':tertiary_schools, 
		'universities':universities, 
		'all_trtransfer':all_trtransfer, 
		'all_deotransfer':all_deotransfer,
		'primary_labels': primary_labels,
		'primary_data': primary_data,
		'secondary_labels': secondary_labels,
		'secondary_data': secondary_data,
		'tertiary_labels': tertiary_labels,
		'tertiary_data': tertiary_data,
		'university_labels': university_labels,
		'university_data': university_data, }
	return render(request, 'ministry/home.html', context)

def pie_chart(request):
	labels = []
	data = []

	queryset = School.objects.values('founder__own_type').annotate(total_schools=Count('founder')).filter(level=2)
	for city in queryset:
		labels.append(city['founder__own_type'])
		data.append(city['total_schools'])

	return render(request, 'home.html', {
		'labels': labels,
		'data': data,
	})

def communication(request):
	if request.method == 'POST':
		form = CommunicationCreateForm(request.POST, request.FILES)
		if form.is_valid():
			form.instance.user = request.user
			form.save()
			messages.success(request, f'New communication has been published.')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		form = CommunicationCreateForm()
	context = {
		'form':form,
		'title':'Communication',
		'submenu':'Communication',
		'communications':Communication.objects.all()
	}
	return render(request, 'ministry/communication.html', context)

def update_communication(request, pk):
	com = Communication.objects.get(pk=pk)
	if request.method == 'POST':
		form = CommunicationCreateForm(request.POST, request.FILES, instance=com)
		if form.is_valid():
			form.instance.user = request.user
			form.save()
			messages.success(request, f'The communication has been updated.')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		form = CommunicationCreateForm(instance=com)
	context = {
		'form':form,
		'com':com,
		'title':'Communication',
		'submenu':'Communication',
		'communications':Communication.objects.all()
	}
	return render(request, 'ministry/communication.html', context)

def download_resource(request):
	if request.method == 'POST':
		form = DownloadResourceCreateForm(request.POST, request.FILES)
		if form.is_valid():
			form.instance.user = request.user
			form.save()
			messages.success(request, f'New resource has been published.')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		form = DownloadResourceCreateForm()
	context = {
		'form':form,
		'title':'Communication',
		'submenu':'Resources',
		'resources':DownloadResource.objects.all()
	}
	return render(request, 'ministry/resources.html', context)

def update_download_resource(request, pk):
	resource = DownloadResource.objects.get(pk=pk)
	if request.method == 'POST':
		form = DownloadResourceCreateForm(request.POST, request.FILES, instance=resource)
		if form.is_valid():
			form.instance.user = request.user
			form.save()
			messages.success(request, f'The resource has been updated.')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		form = DownloadResourceCreateForm(instance=resource)
	context = {
		'form':form,
		'title':'Communication',
		'submenu':'Resources',
		'resources':DownloadResource.objects.all()
	}
	return render(request, 'ministry/resources.html', context)

class DistrictUploadView(FormView):
	template_name = 'ministry/upload_record.html'
	form_class = UploadDistrict
	success_url = '/ministry/upload_district/'

	def form_valid(self, form):
		form.process_data()
		return super().form_valid(form)

class SchoolUploadView(FormView):
	template_name = 'ministry/upload_record.html'
	form_class = UploadSchool
	success_url = '/ministry/upload_school/'

	def form_valid(self, form):
		form.process_data()
		return super().form_valid(form)

class SecondarySchoolUploadView(FormView):
	template_name = 'ministry/upload_record.html'
	form_class = UploadSecondarySchool
	success_url = '/ministry/upload_secondary_school/'

	def form_valid(self, form):
		form.process_data()
		return super().form_valid(form)

class TertiarySchoolUploadView(FormView):
	template_name = 'ministry/upload_record.html'
	form_class = UploadTertiarySchool
	success_url = '/ministry/upload_tertiary_school/'

	def form_valid(self, form):
		form.process_data()
		return super().form_valid(form)

class CountyUploadView(FormView):
	template_name = 'ministry/upload_record.html'
	form_class = UploadCounty
	success_url = '/ministry/upload_county/'

	def form_valid(self, form):
		form.process_data()
		return super().form_valid(form)

class SubCountyUploadView(FormView):
	template_name = 'ministry/upload_record.html'
	form_class = UploadSubCounty
	success_url = '/ministry/upload_subcounty/'

	def form_valid(self, form):
		form.process_data()
		return super().form_valid(form)

class ParishUploadView(FormView):
	template_name = 'ministry/upload_record.html'
	form_class = UploadParish
	success_url = '/ministry/upload_parish/'

	def form_valid(self, form):
		form.process_data()
		return super().form_valid(form)

class ServiceProviderUploadView(FormView):
	template_name = 'ministry/upload_record.html'
	form_class = UploadServiceProvider
	success_url = '/ministry/upload_service_provider/'

	def form_valid(self, form):
		form.process_data()
		return super().form_valid(form)

class UACEUploadView(FormView):
	template_name = 'ministry/upload_record.html'
	form_class = UploadUACE
	success_url = '/ministry/upload_uace/'

	def form_valid(self, form):
		form.process_data()
		return super().form_valid(form)

class UCEUploadView(FormView):
	template_name = 'ministry/upload_record.html'
	form_class = UploadUCE
	success_url = '/ministry/upload_uce/'

	def form_valid(self, form):
		form.process_data()
		return super().form_valid(form)

class UPEUploadView(FormView):
	template_name = 'ministry/upload_record.html'
	form_class = UploadUPE
	success_url = '/ministry/upload_upe/'

	def form_valid(self, form):
		form.process_data()
		return super().form_valid(form)