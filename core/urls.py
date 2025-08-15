from django.urls import path
from . import views
from .views import comp_page

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('about/', views.about_alcher, name='about_alcher'),
    path('cfa/', views.cfa_register_page, name='cfa_register'),
    path('cfa/register/step1/', views.cfa_register_step1, name='cfa_step1'),  # use cfa_register_step1, not cfa_step1_view
    path('cfa/register/step2/', views.cfa_step2_view, name='cfa_step2'),
    path('cfa/step-3/', views.cfa_step3, name='cfa_step3'),
    path('competitions/', comp_page, name='competitions'),
]
