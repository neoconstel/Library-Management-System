from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, "library/index.html")


def admin_portal(request):
    return render(request, 'library/admin_portal.html')


def student_portal(request):
    return render(request, 'library/student_portal.html')



