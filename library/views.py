from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

from .models import Book, Order
from .forms import BookForm


def home(request):
    return render(request, 'library/index.html')


# def admin_portal(request):
#     books = Book.objects.all() 
#     context = {
#          'books': books,
#          'total_book_titles': books.count(),
#          'total_available_books': sum([book.quantity for book in books])
#     }
#     return render(request, 'library/admin_portal.html', context=context)


def student_portal(request):
    return render(request, 'library/student_portal.html')


class AddBooks(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('admin-portal')


class AdminPortal(ListView):
    model = Book
    template_name = 'library/admin_portal.html'
    context_object_name = 'books'


class ViewOrders(ListView):
    model = Order
    context_object_name = 'orders'



