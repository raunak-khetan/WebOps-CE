from django.urls import path
from .import views

urlpatterns = [
    path('', views.prelimspage, name='prelimspage'),
    path('competitions/<str:city_name>/', views.citypage, name='citypage'),
    path('competitions/<str:city_name>/<str:event_name>/', views.detailspage, name='detailspage'),
    path('competitions/<str:city_name>/<str:event_name>/register', views.registrationpage, name='registrationpage'),
    path('get-events/<str:city_name>/', views.get_city_events, name='get_city_events'),
    path('api/cities/', views.city_list, name='city_list'),
]