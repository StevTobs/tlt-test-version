from django.urls import path

from . import views

urlpatterns = [
    path('staff-dashboard', views.staff_dashboard, name="staff-dashboard"),
]
