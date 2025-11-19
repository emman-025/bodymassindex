from django.urls import path
from . import views

urlpatterns = [
    path('', views.bmi_form, name='bmi_form'), 
    
]