from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns = [
    path('api/get-employees/', views.get_employees),
    path('api/add-employee/', views.add_employee_json),
    path('form/', views.add_employee_details, name='details'),
    path('',views.index , name='index'),
    path('delete/<int:id>/', views.delete_employee, name='delete_employee'),
    path('api/update-employee/<str:emp_id>/', views.update_employee),
    path('api/delete-employee/<str:emp_id>/', views.delete_employee_json),
    path('api/check-email/', views.check_email_exists),
    path('api/check-phone/', views.check_phone_exists),
    path('api/signup/', views.signup_user),
    path('api/login/', views.login_user),
]
