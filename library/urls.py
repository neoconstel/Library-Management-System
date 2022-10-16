from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('librarian/', views.AdminPortal.as_view(), name='admin-portal'),
    path('librarian/add-books/', views.BookCreate.as_view(), name='add-books'),
    path('librarian/view-books/<int:pk>/', views.BookDetail.as_view(), name='view-books'),
    path('librarian/update-books/<int:pk>/', views.BookUpdate.as_view(), name='update-books'),
    path('librarian/delete-books/<int:pk>/', views.BookDelete.as_view(), name='delete-books'),
    path('librarian/view-orders/', views.ViewOrders.as_view(), name='view-orders'),


    path('student/', views.StudentPortal.as_view(), name='student-portal'),
]