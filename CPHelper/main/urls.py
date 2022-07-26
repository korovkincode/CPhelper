from django.urls import path
from . import views

urlpatterns = [
	path('', views.index),
	path('dashboard/', views.dashboard),
	path('contests/', views.contests),
	path('signup/', views.signup),
	path('login/', views.login),
	path('logout/', views.logout),
	path('settings/', views.settings),
]