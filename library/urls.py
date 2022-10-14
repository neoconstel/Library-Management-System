from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('librarian/', views.AdminPortal.as_view(), name='admin-portal'),
    path('librarian/add-books/', views.AddBooks.as_view(), name='add-books'),
    path('librarian/view-orders/', views.ViewOrders.as_view(), name='view-orders'),


    path('student/', views.student_portal, name='student-portal')
]