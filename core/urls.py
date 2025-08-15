from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('about/', views.about_alcher, name='about_alcher'),

    # CFA Registration Steps
    path('cfa/', views.cfa_register_page, name='cfa_register'),
    path('cfa/register/step1/', views.cfa_register_step1, name='cfa_step1'),
    path('cfa/register/step2/', views.cfa_step2_view, name='cfa_step2'),
    path('cfa/step-3/', views.cfa_step3, name='cfa_step3'),

    # Competitions page
    path('competitions/', views.comp_page, name='competitions'),
]
