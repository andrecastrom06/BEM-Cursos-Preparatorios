from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.def_login, name='login'),
    path('principal/', views.principal, name='principal'),
]
