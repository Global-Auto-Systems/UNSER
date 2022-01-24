import io
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from users.models import *
import datetime
import csv
def current_year():
    return datetime.date.today().year

def year_choices():
	return [(r,r) for r in range(1200, datetime.date.today().year+1)]

class StudentCreateForm(forms.ModelForm):
	class Meta:
		model = Student
		fields =('class_name','age','girls','boys','year')

class RepeaterCreateForm(forms.ModelForm):
	class Meta:
		model = Repeater
		fields =('class_name','girls','boys','year')

class NationalityCreateForm(forms.ModelForm):
	class Meta:
		model = Nationality
		fields =('class_name','country','girls','boys','year')

class ProposedIntakeCreateForm(forms.ModelForm):
	class Meta:
		model = ProposedIntake
		fields =('class_name','girls','boys','year')

class PhysicalStreamCreateForm(forms.ModelForm):
	class Meta:
		model = PhysicalStream
		fields =('class_name','streams','year')

class OrphanCreateForm(forms.ModelForm):
	class Meta:
		model = Orphan
		fields =('class_name','girls','boys','status','year')

class SpecialNeedCreateForm(forms.ModelForm):
	class Meta:
		model = SpecialNeed
		fields =('class_name','girls','boys','status','year')

class NewEntrantCreateForm(forms.ModelForm):
	class Meta:
		model = NewEntrant
		fields =('age','girls','boys','year')

class SeatingAndWritingSpaceCreateForm(forms.ModelForm):
	class Meta:
		model = SeatingAndWritingSpace
		fields =('class_name','pupils','year')

class TransferedStudentCreateForm(forms.ModelForm):
	class Meta:
		model = TransferedStudent
		fields =('class_name','girls','boys','year')

class ExaminationCreateForm(forms.ModelForm):
	class Meta:
		model = Examination
		fields =('class_name','girls','boys','term','year')

class LeftTeacherCreateForm(forms.ModelForm):
	class Meta:
		model = LeftTeacher
		fields =('reason','male','female','year')

class NonTeachingStaffCreateForm(forms.ModelForm):
	class Meta:
		model = NonTeachingStaff
		fields =('staff_type','male','female','year')

class TeacherAllocationCreateForm(forms.ModelForm):
	class Meta:
		model = TeacherAllocation
		fields =('class_name','teachers','year')

class BuildingCreateForm(forms.ModelForm):
	class Meta:
		model = Building
		fields =('room_type','room_state','room_status','permanent','temporary','year')

class UnderConstructionBuildingCreateForm(forms.ModelForm):
	class Meta:
		model = UnderConstructionBuilding
		fields =('room_type','room_completion','rooms','year')

class NeededBuildingCreateForm(forms.ModelForm):
	class Meta:
		model = NeededBuilding
		fields =('room_type','rooms','year')

class WaterAndEnergySourceCreateForm(forms.ModelForm):
	class Meta:
		model = WaterAndEnergySource
		fields =('water_source','distance_to_water_source','energy_source','year')

class LatrineCreateForm(forms.ModelForm):
	class Meta:
		model = Latrine
		fields =('use','state','rooms','year')