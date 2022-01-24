from django import forms
from .models import *
import datetime

class ApplyCreateForm(forms.ModelForm):
	class Meta:
		model = ServiceProvider
		fields =('service','name','capacity','phone','email','address','description')

class ReportCreateForm(forms.ModelForm):
	class Meta:
		model = Report
		fields =('to','school','address','case','covid','name','phone','email','date')