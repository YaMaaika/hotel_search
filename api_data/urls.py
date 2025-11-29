from django.urls import path
from . import views

app_name = 'api_data'

urlpatterns = [
    path('', views.hotel_search, name='hotel_search'),
]
