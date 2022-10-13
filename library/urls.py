from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('librarian/', views.admin_portal, name='admin-portal'),
    path('student/', views.student_portal, name='student-portal')
]