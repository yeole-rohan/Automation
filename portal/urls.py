from django.contrib import admin
from django.urls import path, include
from . import views
from .views import GPRegister, AccountantRegsiter, DirectorRegsiter, ObservarRegsiter

urlpatterns = [
    path('', views.home, name="home"),
    path('accounts/login/',views.login_view, name="login"),
    path('accounts/signup/gp/', GPRegister.as_view(), name="gp"),
    path('accounts/signup/accountant/', AccountantRegsiter.as_view(), name="accountant"),
    path('accounts/signup/director/', DirectorRegsiter.as_view(), name="accountant"),
    path('accounts/signup/observar/', ObservarRegsiter.as_view(), name="ob"),
    path('payments/', views.payments, name="payments"),
    path('dir/', views.director_approve, name="director"),
    path('dir/action/<int:user_id>/', views.director_action, name="dir_action"),
    path('all-payments/', views.accountant_list, name="accountant_list"),
    path('action/<int:user_id>/', views.action, name="action"),
    path('load-taluka/', views.load_taluka, name="ajax_taluka"),
    path('load-panchayat', views.load_panchayat,name="ajax_panchayat"),
    path('two/', views.phase_two, name="two"),
    path('observar/', views.observar, name="observar"),
    path('three/', views.phase_three, name="three"),
    path('four/', views.phase_four, name="four"),
    path('servi/', views.servilance, name="servilance"),
]