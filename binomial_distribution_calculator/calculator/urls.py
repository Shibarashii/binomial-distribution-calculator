from django.urls import path
from . import views

urlpatterns = [
    path('', views.starting_page, name='starting-page'),
    path('tutorial/', views.tutorial, name='tutorials-page'),
    path('faqs/', views.faqs, name='faqs-page'),
    path('members/', views.members, name='members-page'),
    path('calculate/', views.calculate, name='calculate'),
]
