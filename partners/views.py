from django.shortcuts import render, redirect
from ministry.models import *
from .models import *
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.db.models import Sum, Count

def home(request):
	context = {
	'title': 'Home',
	}
	return render(request, 'partners/home.html', context)