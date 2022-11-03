from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('redirect/', views.LoginRedirectView.as_view(), name='login-success'),
    path('signup/', views.SignupView.as_view(), name='signup'),


    path('', views.Home.as_view(), name='home'),
    path('library/management', views.AdminLibrary.as_view(), name='admin-library'),
    path('library/add-books/', views.BookCreate.as_view(), name='add-books'),
    path('library/view-books/<int:pk>/', views.BookDetail.as_view(), name='view-books'),
    path('library/update-books/<int:pk>/', views.BookUpdate.as_view(), name='update-books'),
    path('library/delete-books/<int:pk>/', views.BookDelete.as_view(), name='delete-books'),
    path('library/view-orders/', views.ViewOrders.as_view(), name='view-orders'),


    path('student/dashboard', views.StudentCollections.as_view(), name='student-collections'),
    path('student/create-order/', views.OrderCreate.as_view(), name='create-order'),
    path('student/delete-order/<int:pk>/', views.OrderDelete.as_view(), name='delete-order'),
    path('student/student-library', views.StudentLibrary.as_view(), name='student-library')
]