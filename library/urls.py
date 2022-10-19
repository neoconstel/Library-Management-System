from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('redirect/', views.LoginRedirectView.as_view(), name='login-success'),
    path('signup/', views.SignupView.as_view(), name='signup'),


    path('', views.Home.as_view(), name='home'),
    path('librarian/', views.AdminPortal.as_view(), name='admin-portal'),
    path('librarian/add-books/', views.BookCreate.as_view(), name='add-books'),
    path('librarian/view-books/<int:pk>/', views.BookDetail.as_view(), name='view-books'),
    path('librarian/update-books/<int:pk>/', views.BookUpdate.as_view(), name='update-books'),
    path('librarian/delete-books/<int:pk>/', views.BookDelete.as_view(), name='delete-books'),
    path('librarian/view-orders/', views.ViewOrders.as_view(), name='view-orders'),


    path('student/', views.StudentPortal.as_view(), name='student-portal'),
    path('student/create-order/', views.OrderCreate.as_view(), name='create-order'),
    path('student/delete-order/<int:pk>/', views.OrderDelete.as_view(), name='delete-order'),
    path('student/student-library', views.StudentLibrary .as_view(), name='student-library')
]