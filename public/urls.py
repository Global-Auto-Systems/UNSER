from django.urls import path
from . import views
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='website-home'),
    path('schools/<int:pk>/', views.schools, name='website-schools'),
    path('school/<int:pk>/', views.school, name='school'),
    path('schools/<int:pk>/op_status', views.operation_status, name='website-operation-status'),
    path('schools/<int:pk>/founder', views.founder, name='website-founder'),
    path('schools/<int:pk>/funder', views.funders, name='website-funder'),
    path('schools/<int:pk>/category', views.category, name='website-categories'),
    path('schools/<int:pk>/section', views.section, name='website-sections'),
    path('schools/<int:pk>/reg_status', views.registration_status, name='website-registration-status'),
    path('schools/<int:pk>/access', views.access, name='website-accesses'),
    path('schools/<int:pk>/urban', views.rural_urban, name='website-rural-urban'),
    path('schools/<int:pk>/nearest_school', views.nearest_school, name='website-nearest-school'),
    path('schools/<int:pk>/nearest_deo', views.nearest_deo, name='website-nearest-deo'),
    path('teachers/', views.teachers, name='website-teachers'),
    path('DEOs/', views.deos, name='website-deos'),
    path('results/', views.results, name='website-results'),
    path('marketing/', views.marketing, name='website-marketing'),
    path('service_providers/', views.service_providers, name='service-providers'),
    path('apply/', views.apply, name='apply'),
    path('covid19/', views.covid19, name='covid19'),
    path('report/', views.report, name='report'),
    path('covid19_downloads/<int:pk>/', views.covid19_downloads, name='covid19-downloads'),
    path('communication/', views.communication, name='website-communication'),
    path('resources/', views.resources, name='website-resources'),
    path('results_uace/', views.uace_results, name='results-uace'),
    path('results_uce/', views.uce_results, name='results-uce'),
    path('results_ple/', views.ple_results, name='results-ple'),
    path('settings/', views.settings, name='website-settings'),
    path('slider/', SliderTemplate.as_view(), name='slider'),
    path('slider_main/', SliderMainTemplate.as_view(), name='slider-main'),
    path('search_google/', views.search_google, name='search-google'),

]
